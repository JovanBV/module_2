SQLite
CREATE TABLE addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    addreses VARCHAR(45) NOT NULL
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name VARCHAR(45) NOT NULL
);

CREATE TABLE customers_addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(45) NOT NULL,
    address_id INT REFERENCES addresses(id),
    customers INT REFERENCES customers(id)
);

CREATE TABLE customers_phone (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INT REFERENCES customers(id), 
    phone_number VARCHAR(45) NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    delivery_time TIME NOT NULL,
    customer_id INT REFERENCES customers(id)
);

CREATE TABLE items(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name VARCHAR(45) NOT NULL,
    price DECIMAL(10,4) NOT NULL
);

CREATE TABLE special_requests(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    special_requests VARCHAR(45) NOT NULL
);

CREATE TABLE order_items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INT REFERENCES items(id), 
    special_requests_id INT REFERENCES special_requests(id),
    order_id INT REFERENCES orders(id),
    quantity INT NOT NULL
);

