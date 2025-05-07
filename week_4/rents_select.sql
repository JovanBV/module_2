-- SQLite

SELECT Books.name, Authors.name FROM Books
LEFT JOIN Authors ON Books.author_id = Authors.id

SELECT * From Books
WHERE Books.author_id IS NULL

SELECT Authors.name FROM Authors
LEFT JOIN Books ON Books.author_id = Authors.id
WHERE Books.name IS NULL

SELECT Books.id, Books.name AS 'Not rented books' FROM Books
LEFT JOIN Rents ON Books.id = Rents.BookID
WHERE BookID IS NULL

SELECT Books.id, Books.name AS 'Rented books' FROM Books
LEFT JOIN Rents ON Books.id = Rents.BookID
WHERE BookID IS NOT NULL
GROUP BY Books.id

SELECT Customers.id, Customers.name AS 'Has never rented' FROM Customers
LEFT JOIN Rents ON  Customers.id = Rents.CustomerID
WHERE CustomerID IS NULL

SELECT Books.id, Books.name AS 'Books on state overdue' FROM Books
JOIN Rents ON Rents.BookID = Books.id
WHERE Rents.State = 3