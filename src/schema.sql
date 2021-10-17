CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    level INTEGER,
    name TEXT,
    description TEXT
);