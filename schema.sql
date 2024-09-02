-- schema.sql

CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE borrowers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE borrowing_history (
    id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL,
    borrower_id INTEGER NOT NULL,
    borrow_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books (id),
    FOREIGN KEY (borrower_id) REFERENCES borrowers (id)
);