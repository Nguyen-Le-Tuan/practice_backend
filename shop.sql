-- Table: Products
CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock_quantity INTEGER NOT NULL,
    supplier_id INTEGER,
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);

-- Table: Customers
CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone_number TEXT,
    address TEXT
);

-- Table: Orders
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    total_amount REAL NOT NULL,
    status TEXT NOT NULL, -- e.g., 'Pending', 'Completed', 'Cancelled'
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- Table: OrderItems
CREATE TABLE OrderItems (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Table: Suppliers
CREATE TABLE Suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT NOT NULL,
    contact_person TEXT,
    phone_number TEXT,
    email TEXT UNIQUE,
    address TEXT
);

-- Insert statements for Suppliers table
INSERT INTO Suppliers (supplier_name, contact_person, phone_number, email, address) VALUES
('Tech Gadgets Inc.', 'Alice Smith', '123-456-7890', 'alice.s@techgadgets.com', '101 Tech Way, Silicon Valley'),
('Fashion Wholesalers', 'Bob Johnson', '987-654-3210', 'bob.j@fashionwholesale.com', '202 Style Ave, Fashion City'),
('Book Distributors Co.', 'Charlie Brown', '555-123-4567', 'charlie.b@bookdist.com', '303 Literary Lane, Storyville');

-- Insert statements for Products table
INSERT INTO Products (product_name, description, price, stock_quantity, supplier_id) VALUES
('Smartphone X', 'Latest model with AI features', 799.99, 150, 1),
('Wireless Earbuds Pro', 'Noise-cancelling, long battery life', 149.99, 300, 1),
('Summer Dress', 'Light and comfortable, floral design', 49.99, 100, 2),
('Men''s Jeans', 'Slim fit, durable denim', 69.99, 80, 2),
('The Great Adventure (Novel)', 'Bestselling fantasy novel', 19.99, 250, 3),
('SQL Basics Guide', 'Comprehensive guide for beginners', 35.00, 120, 3);

-- Insert statements for Customers table
INSERT INTO Customers (first_name, last_name, email, phone_number, address) VALUES
('John', 'Doe', 'john.doe@example.com', '111-222-3333', '404 Oak Street, Anytown'),
('Jane', 'Smith', 'jane.smith@example.com', '444-555-6666', '505 Pine Avenue, Otherville'),
('Peter', 'Jones', 'peter.j@example.com', '777-888-9999', '606 Birch Lane, Somewhere');

-- Insert statements for Orders table
-- Note: Dates are TEXT and can be stored in 'YYYY-MM-DD HH:MM:SS' format.
INSERT INTO Orders (customer_id, order_date, total_amount, status) VALUES
(1, '2025-05-28 10:30:00', 949.98, 'Completed'), -- John Doe's order
(2, '2025-05-29 14:00:00', 119.98, 'Pending'),   -- Jane Smith's order
(1, '2025-05-29 09:15:00', 35.00, 'Processing'); -- Another order for John Doe

-- Insert statements for OrderItems table
-- These link specific products to specific orders.
INSERT INTO OrderItems (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 799.99),  -- Order 1: 1x Smartphone X
(1, 2, 1, 149.99),  -- Order 1: 1x Wireless Earbuds Pro
(2, 3, 2, 49.99),   -- Order 2: 2x Summer Dress
(2, 4, 1, 69.99),   -- Order 2: 1x Men's Jeans (Total for order 2 is actually 49.99*2 + 69.99 = 169.97, so update order 2 total_amount later)
(3, 6, 1, 35.00);   -- Order 3: 1x SQL Basics Guide

-- Correction for Order 2 total_amount (calculated from OrderItems)
UPDATE Orders
SET total_amount = (SELECT SUM(quantity * unit_price) FROM OrderItems WHERE order_id = 2)
WHERE order_id = 2;