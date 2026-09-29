CREATE DATABASE IF NOT EXISTS library_management;
USE library_management;
DROP TABLE IF EXISTS borrow_records;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS categories;
-- category table --
CREATE TABLE categories (
   category_id INT AUTO_INCREMENT PRIMARY KEY,
   category_name VARCHAR(100) NOT NULL UNIQUE,
   description VARCHAR(255)
);
-- books table--
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(150) NOT NULL,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    category_id INT NOT NULL,
    total_copies INT NOT NULL,
    available_copies INT NOT NULL,
    published_year INT,
    CONSTRAINT fk_books_category
         FOREIGN KEY (category_id)
         REFERENCES categories(category_id)
         ON UPDATE CASCADE
         ON DELETE RESTRICT,
   CONSTRAINT chk_book_total_copies CHECK (total_copies >= 0),
   CONSTRAINT chk_book_available_copies CHECK (available_copies
    >= 0),
    CONSTRAINT chk_book_published_year CHECK (published_year IS
    NULL OR published_year BETWEEN 1000 AND 2100)
);
DESCRIBE categories;
DESCRIBE books;

-- member table --
CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    address VARCHAR(255),
    membership_date DATE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT chk_member_phone CHECK (phone REGEXP '^[0-9]{10}$')
);
DESCRIBE members;
-- borrow recors --
CREATE TABLE borrow_records (
    borrow_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE NULL,
    status ENUM('Borrowed', 'Returned', 'Overdue') NOT NULL DEFAULT
    'Borrowed',
    CONSTRAINT fk_borrow_book FOREIGN KEY (book_id)
    REFERENCES books(book_id) ON UPDATE CASCADE ON DELETE 
    RESTRICT,
    CONSTRAINT fk_borrow_member FOREIGN KEY (member_id)
    REFERENCES members(member_id) ON UPDATE CASCADE ON DELETE
    RESTRICT,
    CONSTRAINT chk_borrow_dates CHECK (due_date >= borrow_date),
    CONSTRAINT chk_return_date CHECK (return_date IS NULL OR 
    return_date >= borrow_date)
);
DESCRIBE borrow_records;

INSERT INTO categories (category_name, description)
VALUES
('Fiction', 'Fictional books and novels'),
('Science', 'Science and technology books'),
('Programming', 'Programming and computer science books'),
('History', 'Historical books and references');

INSERT INTO books (title, author, isbn, category_id, total_copies,
available_copies, published_year)
VALUES
('The Guide', 'R.K. Narayan', '9780000000001', 1, 5, 5, 1958),
('Wings of Fire', 'A.P.J Abdul Kalam', '9780000000002', 4, 3, 3, 
1999),
('Python Programming', 'Mark Lutz', '9780000000003', 3, 4, 4, 
2013),
('Clean Code', 'Robert C.Martin', '9780000000004', 3, 5, 5, 2008),
('A Brief History of Time', 'Stephen Hawking', '9780000000005', 2, 
2, 2, 1988);

INSERT INTO members (name, email, phone, address,
membership_date, is_active)
VALUES
('Sumiya', 'sumiya@123.com', '9876543210', 'Andhra Pradesh',
CURDATE(), TRUE),
('Anjali', 'anjali@401.com', '9845627307', 'Chennai', 
CURDATE(), TRUE),
('Nikhila', 'nikhila@456.com', '9876543212', 'Bangalore', 
CURDATE(), TRUE);

INSERT INTO borrow_records (book_id, member_id, borrow_date,
due_date, return_date, status)
VALUES
(1, 1, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY), NULL,
'Borrowed'),
(2, 2, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY), CURDATE(),
'Returned'),
(3, 3, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY), NULL,
'Borrowed');

SELECT * FROM categories;
SELECT * FROM books;
SELECT * FROM members;
SELECT * FROM borrow_records;
Delete FROM borrow_records WHERE member_id = 2;
SELECT * FROM borrow_records WHERE member_id = 2;