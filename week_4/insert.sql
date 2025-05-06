-- SQLite
INSERT INTO addresses (addreses) VALUES ('123 Main St'), ('456 Elm St');

INSERT INTO customers (name) VALUES ('Alice'), ('Bob');

INSERT INTO special_requests (special_requests) VALUES ('Sin cebolla'), ('Extra queso');

INSERT INTO items (name, price) VALUES ('Pizza', 8.99), ('Hamburguesa', 5.50);

INSERT INTO customers_addresses (name, address_id, customers) VALUES
('Casa de Alice', 1, 1),
('Casa de Bob', 2, 2);

INSERT INTO customers_phone (customer_id, phone_number) VALUES
(1, '123-456-7890'),
(2, '098-765-4321');

-- 7. Órdenes
INSERT INTO orders (delivery_time, customer_id) VALUES
('18:30', 1),
('19:00', 2);

INSERT INTO order_items (item_id, special_requests_id, order_id, quantity) VALUES
(1, 1, 1, 2),  -- 2 Pizzas sin cebolla en orden 1
(2, 2, 2, 1);  -- 1 Hamburguesa con extra queso en orden 2
