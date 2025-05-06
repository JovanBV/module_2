SQLite
SELECT * FROM products;

SELECT * FROM products WHERE price > 50000;

SELECT product_id, amount_per_product FROM product_shopping_cart GROUP BY id

SELECT * FROM product_shopping_cart GROUP BY shopping_cart_id

SELECT * FROM bills GROUP BY shopping_cart_id

SELECT * FROM bills ORDER BY total_amount DESC

SELECT * FROM bills WHERE bill_number = 1001

