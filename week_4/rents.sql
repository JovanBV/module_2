-- SQLite

CREATE TABLE Authors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(45)
);

CREATE TABLE Customers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(45) NOT NULL,
    email VARCHAR(45) NOT NULL
);

CREATE TABLE Books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(45) NOT NULL,
    author_id INT REFERENCES Authors(id)
);

CREATE TABLE States(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state VARCHAR(45) UNIQUE
);

CREATE TABLE Rents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    BookID INT REFERENCES Books(id),
    CustomerID INT REFERENCES Customers(id),
    State INT REFERENCES States(id)
);