CREATE TABLE polls (
    poll_id VARCHAR(50) PRIMARY KEY,
    question VARCHAR(255) NOT NULL,
    options TEXT,
    votes TEXT
);
