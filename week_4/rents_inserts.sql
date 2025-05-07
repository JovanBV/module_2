SQLite
INSERT INTO Books(name, author_id) VALUES
('Don quijote', 1),
('La Divina Comedia', 2),
('Vagabond 1-3', 3),
('Dragon Ball 1', 4);

INSERT INTO Books(name) VALUES
('The Book of the 5 Rings');

INSERT INTO Authors(name) VALUES
('Miguel de Cervantes'),
('Dante Alighieri'),
('Takehiko Inoue'),
('Akira Toriyama'),
('Walt Disney');

INSERT INTO Customers(name, email) VALUES
('John Doe', 'j.doe@email.com'),
('Jane Doe', 'jane@doe.com'),
('Luke Skywalker', 'darth.son@email.com');

INSERT INTO States(state) VALUES
('Returned'),
('On time'),
('Overdue');

INSERT INTO Rents(BookID, CustomerID, state) VALUES
(1,2,1),
(2,2,1),
(1,1,2),
(3,1,2),
(2,2,3);