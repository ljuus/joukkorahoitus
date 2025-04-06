CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    target_sum INTEGER,
    user_id INTEGER REFERENCES users,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE donations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    item_id INTEGER REFERENCES items,
    amount INTEGER,
    donation_date DATETIME DEFAULT CURRENT_TIMESTAMP
)