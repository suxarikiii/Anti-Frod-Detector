-- datasets
CREATE TABLE IF NOT EXISTS datasets (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    original_filename VARCHAR(255),
    status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE
);

-- uploaded_files
CREATE TABLE IF NOT EXISTS uploaded_files (
    id UUID PRIMARY KEY,
    dataset_id UUID REFERENCES datasets(id),
    file_path VARCHAR(500),
    file_type VARCHAR(50),
    uploaded_at TIMESTAMP WITH TIME ZONE
);

-- analysis_jobs
CREATE TABLE IF NOT EXISTS analysis_jobs (
    id UUID PRIMARY KEY,
    dataset_id UUID REFERENCES datasets(id),
    status VARCHAR(50),
    current_step VARCHAR(50),
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);
