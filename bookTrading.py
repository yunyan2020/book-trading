import requests
from api import User, Book,Book_view
import csv


def url(route: str):
    return f"http://127.0.0.1:8000{route}"


def get_all_users():
    users = []
    res = requests.get(url("/users"))
    if res.status_code != 200:
        return []
    for user in res.json():
        user = User(**user)
        print("_________________")
        print(f"ID: {user.id}")
        print(f"username: {user.username}")
        print(f"password: {user.password}")
        users.append(user)
    return users


def hasSameUsernameFunction(username: str):
    res = requests.get(url(f"/user/{username.strip()}"))
    print(f"res is : {res.json}")
    findUsername = len(res.json()) > 0
    print(f"find user name: {findUsername}")
    if not res.status_code == 200:
        return
    return findUsername


def register():
    print("Customer register")
    print("")
    print("Register a new customer")
    username = input(str("Customer username: "))
    password = input(str("Customer password: "))
    hasUsername = hasSameUsernameFunction(username)
    while hasUsername == True:
        print("The username has been used. Please enter another username")
        username = input(str("Customer username: "))
        password = input(str("Customer password: "))
        print(username)
        hasUsername = hasSameUsernameFunction(username)

    new_user = User(username=username, password=password)
    print(new_user)
    res = requests.post(url("/register"), json=new_user.dict())
    print(res)


def getCredientials(username: str):
    res = requests.get(url(f"/user/{username.strip()}"))
    if not res.status_code == 200:
        return
    return res.json()


def saveLoinInfo(user: User):
    res = requests.post(url("/login"), json=user.dict())
    if res.status_code == 200:
        print("Login successful")


def logoutExistedUser():
    res = requests.delete(url("/login"))
    if res.status_code != 200:
        return


def login():
    print("Customer login")
    print("")
    username = input(str("Customer username: "))
    password = input(str("Customer password: "))
    credientials = getCredientials(username)[0]
    stored_user = User(**credientials)
    user = User(username=username, password=password,id=stored_user.id)
    print(f"user :{user}")
    if username == stored_user.username and password == stored_user.password:
        logoutExistedUser()
        saveLoinInfo(user)
    else:
        print("Bad credentials")


def import_authors_csv_data():
    with open("authors.csv", "r") as f:
        authors = csv.DictReader(f)
        import_row = 0
        for row in authors:
            author = {"firstName": row["firstName"], "lastName": row["lastName"]}
            res = requests.post("http://localhost:8000/import-authors", json=author)
            if res.status_code == 200:
                import_row += 1
                print(f"Imported the {import_row}th rows authors data successfully")
            else:
                print(f"Imported failed")

def import_book_csv_data():
    with open("books.csv", "r") as f:
        books = csv.DictReader(f)
        import_row = 0
        for row in books:
            book = {
                "ISBN": row["ISBN"],
                "title": row["title"],
                "authorId": row["authorId"],
                "price": row["price"],
            }
            res = requests.post("http://localhost:8000/import-books", json=book)
            if res.status_code == 200:
                import_row += 1
                print(f"Imported the {import_row}th rows books data successfully")
            else:
                print(f"Imported failed")

def get_all_books():
     books = []
     res = requests.get(url("/books"))
     if res.status_code != 200:
        return []
     for book in res.json():
        book = Book_view(**book)
        print("_________________")
        print(f"Book ID: {book.id} ISBN: {book.ISBN} Title:{book.title} Author:{book.author} Price: {book.price}")
        books.append(book)
     return books

def get_book_by_id(id:int):
    res = requests.get(url(f"/book/{id}"))
    if res.status_code != 200:
        return []   
    return res.json()

def get_customer_code():
    res = requests.get(url(f"/current_login"))
    if res.status_code != 200:
        return []   
    return res.json()

def order_books():
    get_all_books()
    bookId = input("Please input your Book ID: ")
    bookId = bookId.strip()
    if not str.isdigit(bookId):
        print("Ids are integers")
        return
    order_book = get_book_by_id(bookId)
    while  order_book == []:
        print("There is no such book")
        bookId = input("Please input your Book ID: ")
        bookId = bookId.strip()
        if not str.isdigit(bookId):
            print("Ids are integers")
        ordered_book = get_book_by_id(bookId)

    for book in ordered_book:
        book = Book_view(**book)
        print(f"Book ID: {book.id} ISBN: {book.ISBN} Title:{book.title} Author:{book.author} Price: {book.price}")
        
    print(book)
    
    current_login = get_customer_code()
   



