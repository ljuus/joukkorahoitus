CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    target_sum INTEGER,
    user_id INTEGER REFERENCES users,
    category_id INTEGER REFERENCES categories,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE donations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    item_id INTEGER REFERENCES items,
    amount NUMERIC,
    donation_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE item_images (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    image BLOB 
);