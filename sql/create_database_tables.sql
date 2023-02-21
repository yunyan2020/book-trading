use master;
if not exists(
select name
from sys.databases
where name= N'bookTrading')
create database "bookTrading";

use bookTrading;

create table users (
	id INT IDENTITY(1000,1)NOT NULL PRIMARY KEY,
	username VARCHAR(255),
	password VARCHAR(255)
); 

create table currentLogin (
	id INT IDENTITY(1,1)NOT NULL PRIMARY KEY,
	customerId INT NOT NULL,
	username VARCHAR(255),
	loginDate datetime
); 


create table authors (
	authorId INT IDENTITY(100,1) NOT NULL PRIMARY KEY,
	firstName VARCHAR(255)  NOT NULL,
	lastName VARCHAR(255)  NOT NULL
);

create table books (
	id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
	ISBN VARCHAR(20) NOT NULL UNIQUE, 
	title VARCHAR(50) NOT NULL,
	authorId INT,
	price DECIMAL(5,2) NOT NULL,
	CONSTRAINT fk_author FOREIGN KEY (authorId) 
    REFERENCES authors(authorId)
)



create table orders (
	orderNo INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
	customerId INT NOT NULL,
	ISBN VARCHAR(20) NOT NULL,
	quantity INT NOT NULL,
	salesPrice DECIMAL(5,2) NOT NULL,
	salesDate DATE NOT NULL,
	CONSTRAINT fk_orders_customer FOREIGN KEY (customerId) 
    REFERENCES users(id),
	CONSTRAINT fk_orders_book FOREIGN KEY (ISBN) 
    REFERENCES books(ISBN)
);

