CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    created TIMESTAMP,
    is_admin BOOLEAN
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    level INTEGER,
    name TEXT,
    description TEXT,
    text_to_write TEXT
);

CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    exercise_id INTEGER REFERENCES exercises,
    used_time INTEGER,
    adjusted_time INTEGER,
    errors INTEGER,
    sent_at TIMESTAMP,
    approved BOOLEAN
);

