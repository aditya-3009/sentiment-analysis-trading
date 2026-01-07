-- Users table (students / traders)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Raw text sources (news, earnings calls, etc.)
CREATE TABLE IF NOT EXISTS raw_text_data (
    id SERIAL PRIMARY KEY,
    source TEXT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Preprocessed text
CREATE TABLE IF NOT EXISTS preprocessed_text (
    id SERIAL PRIMARY KEY,
    raw_text_id INT REFERENCES raw_text_data(id),
    cleaned_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sentiment analysis results
CREATE TABLE IF NOT EXISTS sentiment_scores (
    id SERIAL PRIMARY KEY,
    preprocessed_text_id INT REFERENCES preprocessed_text(id),
    sentiment TEXT NOT NULL,
    score FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trading signals generated from sentiment
CREATE TABLE IF NOT EXISTS trading_signals (
    id SERIAL PRIMARY KEY,
    sentiment_score_id INT REFERENCES sentiment_scores(id),
    signal TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS text_features (
    id SERIAL PRIMARY KEY,
    preprocessed_text_id INT REFERENCES preprocessed_text(id),
    token_count INT,
    avg_word_length FLOAT,
    has_financial_keyword BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
