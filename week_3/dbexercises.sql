SQLite

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(25) NOT NULL,
    price DECIMAL(13,4) NOT NULL,
	entry_date DATE NOT NULL,
	brand VARCHAR(25) NOT NULL
);


CREATE TABLE product_shopping_cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INT REFERENCES products(id),
    shopping_cart_id INT REFERENCES shopping_cart(id), 
    amount_per_product INT NOT NULL
);

CREATE TABLE shopping_cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT REFERENCES users(id)
);

CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_email VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_number INT NOT NULL,
    buy_date DATE NOT NULL, 
    total_amount DECIMAL(13,4) NOT NULL, 
    shopping_cart_id INT REFERENCES shopping_cart(id)
);

ALTER TABLE users
    ADD cellphone VARCHAR(20)


INSERT INTO users (user_email, cellphone) VALUES 
('alice@example.com', '+50688881234'),
('bob@example.com', '+50670112233'),
('carol@example.com', '+50660009988');

INSERT INTO shopping_cart (user_id) VALUES 
(1),    --Alice shopping cart
(2),    --Bob shopping cart
(3);    --Carol shopping carrt

INSERT INTO bills (bill_number, buy_date, total_amount, shopping_cart_id) VALUES 
(1001, '2025-04-30', 940.9899, 1),
(1002, '2025-04-29', 499.5000, 2),
(1003, '2025-04-28', 199.9500, 3);



INSERT INTO product_shopping_cart (product_id, amount_per_product, shopping_cart_id) VALUES 
(1, 4,1),     --Alice
(2, 12,2),     --Bob 
(3, 5,3),     --Carol
(4, 1,1);     --Alice

INSERT INTO products (name, price, entry_date, brand) VALUES 
('Laptop Lenovo', 850.9999, '2025-04-01', 'Lenovo'),
('Smartphone Samsung', 499.5000, '2025-03-15', 'Samsung'),
('Headphones Sony', 199.9500, '2025-04-20', 'Sony'),
('Keyboard Logitech', 89.9900, '2025-04-25', 'Logitech');


