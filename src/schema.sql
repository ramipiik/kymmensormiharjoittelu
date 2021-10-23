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

CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    exercise_id INTEGER REFERENCES users,
    used_time INTEGER,
    adjusted_time INTEGER,
    sent_at TIMESTAMP
);

