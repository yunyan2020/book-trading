from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

# from db import DB
from mssql_db import DB


class User(BaseModel):
    id: int = None
    username: str
    password: str


class Book(BaseModel):
    id: int = None
    ISBN: str
    title: str
    authorId: int
    price: float

class Book_view(BaseModel):
    id: int = None
    ISBN: str
    title: str
    author: str
    price: float


class Author(BaseModel):
    id: int = None
    firstName: str
    lastName: str

class Customer(BaseModel):
    customerId: int = None
    username: str
    password: str

class Order(BaseModel):
    orderNo: int = None
    customerId: int
    ISBN       :str
    quantity :int
    salesPrice:float

app = FastAPI()
# db = DB("todo.db")
db = DB()


@app.get("/")
def root():
    return "Hello and welcome to book trading system!"


@app.get("/users")
def get_all_users():
    get_query = """
    SELECT * FROM users
    """
    data = db.call_db(get_query)
    users = [
        User(id=id, username=username, password=password)
        for id, username, password in data
    ]
    return users


@app.post("/register")
def register_customer(user: User):
    insert_query = """
    INSERT INTO users (username,password)
    VALUES (?,?)
    """
    db.call_db(insert_query, user.username, user.password)
    return "Adds a user"


@app.delete("/login")
def delete_login():
    delete_query = """
    DELETE FROM currentLogin 
    """
    db.call_db(delete_query)
    return True


@app.post("/login")
def login_customer(user: User):
    login_date = datetime.now()
    insert_query = """
    INSERT INTO currentLogin (username,customerId,password,loginDate)
    VALUES (?,?,?,?)
    """
    db.call_db(insert_query, user.username,user.id, user.password, login_date)
    return "Login a user"



@app.get("/user/{username}")
def get_user_by_username(username: str):
    get_user_query = """
    SELECT * FROM users
    WHERE username=?
    """
    data = db.call_db(get_user_query, username)
    users = [
        User(id=id, username=username, password=password)
        for id, username, password in data
    ]
    return users


@app.post("/import-books")
async def import_books(book: Book):
    save_books_query = """
    INSERT INTO books (ISBN, title, authorId, price) VALUES (?, ?, ?, ?)
    """
    db.call_db(save_books_query, book.ISBN, book.title, book.authorId, book.price)
    return {"message": "Books data imported to database successfully!"}


@app.post("/import-authors")
async def import_authors(author: Author):
    save_authors_query = """
    INSERT INTO authors (firstName, lastName) VALUES (?, ?)
    """
    db.call_db(save_authors_query, author.firstName, author.lastName)
    return {"message": "Authors data imported to database successfully!"}


@app.get("/books")
def get_all_books():
    get_query = """   
    SELECT b.id,b.ISBN, b.title,STRING_AGG(a.firstName + ' ' + a.lastName, ',')   as author,b.price
    FROM books AS b, authors AS a
    WHERE a.authorId = b.authorID
    GROUP BY b.id, b.ISBN,b.title,b.price
    """
    data = db.call_db(get_query)
    books = [
        Book_view(id=id, ISBN=ISBN, title=title,author=author,price=price)
        for id, ISBN, title,author,price in data
    ]    
    return books


@app.get("/book/{id}")
def get_book_by_id(id: int):
    get_book_query = """
    SELECT b.id,b.ISBN, b.title,STRING_AGG(a.firstName + ' ' + a.lastName, ',')   as author,b.price
    FROM books AS b, authors AS a
    WHERE a.authorId = b.authorID
    AND b.id = ?
    GROUP BY b.id, b.ISBN,b.title,b.price
    """
    data = db.call_db(get_book_query, id)
    books = [
        Book_view(id=id, ISBN=ISBN, title=title,author=author,price=price)
        for id, ISBN, title,author,price in data
    ]    
    return books

@app.get("/current_login")
def get_current_login():
    get_current_login_query = """
    SELECT * FROM currentLogin
    """
    data = db.call_db(get_current_login_query)
    current_login = [
        Customer(customerId=customerId, username=username, password=password)
        for id,customerId, username, password,login_date in data
    ]
    return current_login

@app.post("/order")
def save_order(order: Order):
    insert_query = """
    INSERT INTO orders (customerId,ISBN,quantity,salesPrice,salesDate)
    VALUES (?,?,?,?,?)
    """     
    salesDate = datetime.now()
    db.call_db(insert_query, order.customerId,order.ISBN, order.quantity,order.salesPrice,salesDate)
    return "Order books"

@app.put("/user")
def change_password(user: User):
    update_query = """
    UPDATE users
    SET  password = ?
    FROM users
    WHERE username = ?
    """     
   
    db.call_db(update_query,user.password,user.username)
    return "Password changed"

@app.delete("/order/{order_no}")
def delete_order(order_no: int):
    delete_query = """
    DELETE FROM orders 
    WHERE orderNo = ?
    """
    db.call_db(delete_query,order_no)
    return True

@app.get("/order/{order_no}")
def get_order_by_id(order_no: int):
    get_query = """
    SELECT * FROM orders
    WHERE orderNo = ?
    """     
    data = db.call_db(get_query, order_no) 
    order = [
        Order(orderNo=orderNo, customerId=customerId, ISBN=ISBN,quantity=quantity,salesPrice=salesPrice,salesDate=salesDate)
        for orderNo, customerId, ISBN,quantity,salesPrice,salesDate in data
    ]    
    return order