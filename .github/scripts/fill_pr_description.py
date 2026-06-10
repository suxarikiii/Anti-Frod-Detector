import json
import os
import pathlib
import sys
import urllib.error
import urllib.request


GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
PR_NUMBER = os.environ["PR_NUMBER"]

GITHUB_API_URL = os.environ.get("GITHUB_API_URL", "https://api.github.com")
GITHUB_MODEL = os.environ.get("GITHUB_MODEL", "openai/gpt-4.1-mini")

OWNER, REPO = GITHUB_REPOSITORY.split("/", 1)

MAX_DIFF_CHARS = 55_000
PR_TEMPLATE_PATH = pathlib.Path(".github/pull_request_template.md")


def github_json_request(
    method: str,
    url: str,
    body: dict | None = None,
    extra_headers: dict | None = None,
) -> dict:
    data = None

    if body is not None:
        data = json.dumps(body).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if extra_headers:
        headers.update(extra_headers)

    request = urllib.request.Request(
        url=url,
        data=data,
        method=method,
        headers=headers,
    )

    try:
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")

            if not response_body:
                return {}

            return json.loads(response_body)

    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {error.code} while calling {url}\n{error_body}"
        ) from error


def github_text_request(
    method: str,
    url: str,
    accept_header: str,
) -> str:
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": accept_header,
        "X-GitHub-Api-Version": "2022-11-28",
    }

    request = urllib.request.Request(
        url=url,
        method=method,
        headers=headers,
    )

    try:
        with urllib.request.urlopen(request) as response:
            return response.read().decode("utf-8", errors="replace")

    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {error.code} while calling {url}\n{error_body}"
        ) from error


def get_pull_request() -> dict:
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}"
    return github_json_request("GET", url)


def get_pull_request_diff() -> str:
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}"

    diff = github_text_request(
        method="GET",
        url=url,
        accept_header="application/vnd.github.v3.diff",
    )

    if len(diff) > MAX_DIFF_CHARS:
        return (
            diff[:MAX_DIFF_CHARS]
            + "\n\n[Diff truncated because it is too large.]"
        )

    return diff


def read_pull_request_template() -> str:
    if PR_TEMPLATE_PATH.exists():
        return PR_TEMPLATE_PATH.read_text(encoding="utf-8")

    return """# Pull Request (domain)

<h2 align="center">Description</h2>

Briefly describe what was changed in this pull request.

---

<h2 align="center">Changes Made</h2>

- 
- 
- 

---

<h2 align="center">Additional Notes</h2>

Add any extra context for reviewers.
"""


def build_prompt(template: str, pr: dict, diff: str) -> tuple[str, str]:
    system_prompt = """
You write pull request descriptions for software projects.

Strict rules:
- Fill the provided pull request template.
- Keep the original headings, HTML tags, separators, and section order.
- Do not add new sections.
- Do not remove existing sections.
- Do not perform code review.
- Do not suggest improvements.
- Do not mention AI, automation, GitHub Models, bots, generated text, or this workflow.
- Describe only what is visible in the pull request title, branches, commits, and diff.
- Do not invent business context that is not visible in the diff.
- Use concise, professional developer style.
- Output only the final Markdown body.
""".strip()

    pr_title = pr.get("title", "")
    source_branch = pr.get("head", {}).get("ref", "")
    target_branch = pr.get("base", {}).get("ref", "")
    existing_body = pr.get("body") or ""

    user_prompt = f"""
Pull request title:
{pr_title}

Source branch:
{source_branch}

Target branch:
{target_branch}

Current pull request body:
```md
{existing_body}
```

Pull request template:
```md
{template}
```

Pull request diff:
```diff
{diff}
```

Task:
Fill the pull request template based on the diff.

Section behavior:
- In Description, write 1 concise paragraph explaining the purpose of the changes.
- In Changes Made, write 3-7 bullet points with concrete changes.
- In Additional Notes, write useful context if visible from the diff. If there is no useful extra context, write "No additional notes."

Return only Markdown.
""".strip()

    return system_prompt, user_prompt


def call_github_models(system_prompt: str, user_prompt: str) -> str:
    url = "https://models.github.ai/inference/chat/completions"

    payload = {
        "model": GITHUB_MODEL,
        "temperature": 0.2,
        "max_tokens": 1200,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    }

    response = github_json_request(
        method="POST",
        url=url,
        body=payload,
        extra_headers={
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )

    try:
        content = response["choices"][0]["message"]["content"]
    except KeyError as error:
        raise RuntimeError(
            "Unexpected GitHub Models response format:\n"
            + json.dumps(response, indent=2, ensure_ascii=False)
        ) from error

    return clean_model_output(content)


def clean_model_output(content: str) -> str:
    content = content.strip()

    if content.startswith("```md"):
        content = content.removeprefix("```md").strip()

    if content.startswith("```markdown"):
        content = content.removeprefix("```markdown").strip()

    if content.startswith("```"):
        content = content.removeprefix("```").strip()

    if content.endswith("```"):
        content = content.removesuffix("```").strip()

    return content


def update_pull_request_body(new_body: str) -> None:
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}"

    github_json_request(
        method="PATCH",
        url=url,
        body={
            "body": new_body,
        },
    )


def main() -> None:
    print(f"Repository: {GITHUB_REPOSITORY}")
    print(f"Pull request: #{PR_NUMBER}")
    print(f"Model: {GITHUB_MODEL}")

    pr = get_pull_request()
    template = read_pull_request_template()
    diff = get_pull_request_diff()

    if not diff.strip():
        print("PR diff is empty. Skipping description generation.")
        return

    system_prompt, user_prompt = build_prompt(
        template=template,
        pr=pr,
        diff=diff,
    )

    new_body = call_github_models(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    if not new_body.strip():
        raise RuntimeError("Generated pull request body is empty.")

    update_pull_request_body(new_body)

    print("Pull request description updated successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)