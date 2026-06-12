import fnmatch
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request


GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
PR_NUMBER = os.environ["PR_NUMBER"]

GITHUB_API_URL = os.environ.get("GITHUB_API_URL", "https://api.github.com")
GITHUB_MODEL = os.environ.get("GITHUB_MODEL", "openai/gpt-4.1-mini")

OWNER, REPO = GITHUB_REPOSITORY.split("/", 1)

MAX_DIFF_CHARS = 8_000
MAX_FILE_DIFF_CHARS = 2_000
MAX_EXISTING_BODY_CHARS = 1_500
MAX_SUMMARY_FILES = 80

PR_TEMPLATE_PATH = pathlib.Path(".github/pull_request_template.md")


EXCLUDED_DIFF_PATTERNS = [
    # Python generated files
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "__pycache__/*",
    "**/__pycache__/*",

    # JVM / Gradle generated or binary files
    "*.class",
    "*.jar",
    "**/build/**",
    "**/.gradle/**",

    # Frontend generated files
    "node_modules/**",
    "**/node_modules/**",
    "dist/**",
    "**/dist/**",
    ".next/**",
    "**/.next/**",
    ".vite/**",
    "**/.vite/**",

    # Lock files can be too noisy for PR description generation
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",

    # IDE / local files
    ".idea/**",
    "**/.idea/**",
    ".vscode/**",
    "**/.vscode/**",

    # Logs and local artifacts
    "*.log",
    "logs/**",
    "**/logs/**",
    "coverage/**",
    "**/coverage/**",

    # Local uploads / runtime storage
    "uploads/**",
    "**/uploads/**",
    "storage/**",
    "**/storage/**",
    "tmp/**",
    "**/tmp/**",
    "temp/**",
    "**/temp/**",
]


DOMAIN_RULES = [
    # Backend services
    ("backend/upload-service/**", "backend"),
    ("backend/scoring-service/**", "backend"),
    ("backend/relations-service/**", "backend"),
    ("backend/graph-affiliation-service/**", "backend"),

    # ML / Data
    ("backend/ml-service/**", "ml"),
    ("ml/**", "ml"),
    ("datasets/**", "data"),
    ("data/**", "data"),

    # Frontend
    ("frontend/**", "frontend"),

    # Infrastructure / DevOps
    ("infra/**", "devops"),
    ("docker-compose.yml", "devops"),
    ("**/docker-compose.yml", "devops"),
    ("Dockerfile", "devops"),
    ("**/Dockerfile", "devops"),
    ("infra/nginx/**", "devops"),
    ("nginx/**", "devops"),

    # CI / GitHub automation
    (".github/workflows/**", "ci"),
    (".github/scripts/**", "ci"),
    (".github/ISSUE_TEMPLATE/**", "ci"),
    (".github/pull_request_template.md", "ci"),
    (".github/PULL_REQUEST_TEMPLATE.md", "ci"),

    # Documentation
    ("README.md", "docs"),
    ("**/README.md", "docs"),
    ("docs/**", "docs"),
    ("*.md", "docs"),
]


def github_json_request(
    method: str,
    url: str,
    body: dict | None = None,
    extra_headers: dict | None = None,
) -> dict | list:
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


def get_pull_request() -> dict:
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}"
    response = github_json_request("GET", url)

    if not isinstance(response, dict):
        raise RuntimeError("Unexpected pull request response format.")

    return response


def get_pull_request_files() -> list[dict]:
    files: list[dict] = []
    page = 1

    while True:
        url = (
            f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}/files"
            f"?per_page=100&page={page}"
        )

        response = github_json_request("GET", url)

        if not isinstance(response, list):
            raise RuntimeError("Unexpected pull request files response format.")

        if not response:
            break

        files.extend(response)
        page += 1

    return files


def should_exclude_file(path: str) -> bool:
    return any(
        fnmatch.fnmatch(path, pattern)
        for pattern in EXCLUDED_DIFF_PATTERNS
    )


def truncate_text(text: str, max_chars: int, message: str) -> str:
    if len(text) <= max_chars:
        return text

    return text[:max_chars] + f"\n\n[{message}]"


def detect_pr_domain(files: list[dict]) -> str:
    domains: set[str] = set()

    for file in files:
        filename = file.get("filename", "")

        if not filename:
            continue

        for pattern, domain in DOMAIN_RULES:
            if fnmatch.fnmatch(filename, pattern):
                domains.add(domain)

    if not domains:
        return "general"

    # Product-code changes are usually more important than docs-only hints.
    if len(domains) > 1 and "docs" in domains:
        domains.remove("docs")

    if domains == {"frontend", "backend"}:
        return "fullstack"

    if "frontend" in domains and "backend" in domains:
        return "fullstack"

    if len(domains) == 1:
        return next(iter(domains))

    return ", ".join(sorted(domains))


def apply_domain_to_template(template: str, domain: str) -> str:
    updated_template = re.sub(
        pattern=r"^# Pull Request\s*\([^)]*\)",
        repl=f"# Pull Request ({domain})",
        string=template,
        count=1,
        flags=re.MULTILINE,
    )

    if updated_template == template and "# Pull Request" not in template:
        return f"# Pull Request ({domain})\n\n{template}"

    return updated_template


def ensure_domain_in_body(body: str, domain: str) -> str:
    updated_body = re.sub(
        pattern=r"^# Pull Request\s*\([^)]*\)",
        repl=f"# Pull Request ({domain})",
        string=body,
        count=1,
        flags=re.MULTILINE,
    )

    if updated_body == body and "# Pull Request" not in body:
        return f"# Pull Request ({domain})\n\n{body}"

    return updated_body


def build_compact_diff(files: list[dict]) -> str:
    if not files:
        return ""

    result: list[str] = []

    result.append("Changed files summary:")

    visible_files = files[:MAX_SUMMARY_FILES]

    for file in visible_files:
        filename = file.get("filename", "")
        status = file.get("status", "")
        additions = file.get("additions", 0)
        deletions = file.get("deletions", 0)
        changes = file.get("changes", 0)

        result.append(
            f"- {filename} ({status}, +{additions}/-{deletions}, {changes} changes)"
        )

    if len(files) > MAX_SUMMARY_FILES:
        result.append(
            f"- ... {len(files) - MAX_SUMMARY_FILES} more files omitted from summary"
        )

    result.append("\nRelevant patches:")

    total_chars = 0

    for file in files:
        filename = file.get("filename", "")

        if not filename:
            continue

        result.append(f"\n--- {filename} ---")

        if should_exclude_file(filename):
            result.append("[Skipped generated, binary, local, or noisy file]")
            continue

        patch = file.get("patch")

        if not patch:
            result.append("[No text patch available]")
            continue

        patch = truncate_text(
            text=patch,
            max_chars=MAX_FILE_DIFF_CHARS,
            message="File diff truncated because it is too large.",
        )

        if total_chars + len(patch) > MAX_DIFF_CHARS:
            result.append("[Remaining diff skipped because total diff is too large.]")
            break

        result.append(patch)
        total_chars += len(patch)

    return "\n".join(result)


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


def build_prompt(
    template: str,
    pr: dict,
    compact_diff: str,
    domain: str,
) -> tuple[str, str]:
    system_prompt = """
You write pull request descriptions for software projects.

Strict rules:
- Fill the provided pull request template.
- Keep the original headings, HTML tags, separators, and section order.
- Keep the exact Pull Request heading domain that is already provided in the template.
- Do not add new sections.
- Do not remove existing sections.
- Do not perform code review.
- Do not suggest improvements.
- Do not mention AI, automation, GitHub Models, bots, generated text, or this workflow.
- Describe only what is visible in the pull request title, branches, commits, changed files, and patches.
- Do not invent business context that is not visible in the pull request.
- Use concise, professional developer style.
- Output only the final Markdown body.
""".strip()

    pr_title = pr.get("title", "")
    source_branch = pr.get("head", {}).get("ref", "")
    target_branch = pr.get("base", {}).get("ref", "")
    existing_body = pr.get("body") or ""

    existing_body = truncate_text(
        text=existing_body,
        max_chars=MAX_EXISTING_BODY_CHARS,
        message="Existing pull request body truncated because it is too large.",
    )

    user_prompt = f"""
Detected pull request domain:
{domain}

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

Pull request changed files and compact diff:
```diff
{compact_diff}
```

Task:
Fill the pull request template based on the changed files and compact diff.

Section behavior:
- Keep the first heading exactly as it appears in the template.
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

    if not isinstance(response, dict):
        raise RuntimeError("Unexpected GitHub Models response format.")

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
    files = get_pull_request_files()

    domain = detect_pr_domain(files)
    print(f"Detected domain: {domain}")

    template = read_pull_request_template()
    template = apply_domain_to_template(template, domain)

    compact_diff = build_compact_diff(files)

    if not compact_diff.strip():
        print("PR diff is empty. Skipping description generation.")
        return

    system_prompt, user_prompt = build_prompt(
        template=template,
        pr=pr,
        compact_diff=compact_diff,
        domain=domain,
    )

    new_body = call_github_models(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    new_body = ensure_domain_in_body(new_body, domain)

    if not new_body.strip():
        raise RuntimeError("Generated pull request body is empty.")

    update_pull_request_body(new_body)

    print("Pull request description updated successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Warning: {error}", file=sys.stderr)
        sys.exit(0)