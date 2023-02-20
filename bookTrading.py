import datetime
import requests
from api import User, Book_view,Customer,Order,Order_view
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
    if username == stored_user.username and password == stored_user.password:
        logoutExistedUser()
        saveLoinInfo(user)
    else:
        print("Bad credentials")


def import_authors_csv_data():
    with open("import/authors1.csv", "r") as f:
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
    with open("import/books1.csv", "r") as f:
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

def get_current_login():
    res = requests.get(url(f"/current_login"))
    if res.status_code != 200:
        return []   
    return res.json()

def save_order(order: Order):
    res = requests.post(url("/order"), json=order.dict())
    if res.status_code == 200:
        print("Save order successful")
    else:
        print("Save order failed")


def order_books():
    #check if it is login
    current_login = get_current_login()
    if current_login == []:
        print("You haven't login. Plese login first!")
        return
    for customer in current_login:
        customer_info =  Customer(**customer)

    get_all_books()
    bookId = input("Please input your Book ID: ")
    bookId = bookId.strip()
    if not str.isdigit(bookId):
        print("Ids are integers")
        return
    ordered_book = get_book_by_id(bookId)
    while  ordered_book == []:
        print("There is no such a book")
        bookId = input("Please input your Book ID: ")
        bookId = bookId.strip()
        if not str.isdigit(bookId):
            print("Ids are integers")
        ordered_book = get_book_by_id(bookId)

    for book in ordered_book:
        book = Book_view(**book)
        print(f"Book ID: {book.id} ISBN: {book.ISBN} Title:{book.title} Author:{book.author} Price: {book.price}")   
    

    quantity = input("Please enter the quantity of books you want to order: ")
    quantity = quantity.strip()
    if not str.isdigit(quantity):
        print("Ids are integers")
        return
    print(f"customerId {customer_info.customerId}") 
    order = Order(customerId=customer_info.customerId, ISBN=book.ISBN,quantity=quantity,salesPrice=book.price)
    save_order(order)


def change_password():
    print("Change password")
    print("")
    password = input(str("New password : "))
    repeat_password = input(str("Verify New Password: "))
    if password != repeat_password:
        print("New password is not match your repeated password!")
        return
    
    current_login = get_current_login()
    if current_login == []:
        print("You haven't login yet! Please login first!")
        return
    for user in current_login:
        login_user =  User(**user)

    user = User(username=login_user.username, password=password)
    res = requests.put(url("/user"), json=user.dict())
    if res.status_code == 200:
        print("Change password successful")
    else:
        print("Change password failed")

def get_order_by_id(order_no:int):
    res = requests.get(url(f"/order/{order_no}"))
    if res.status_code != 200:
        return []   
    return res.json()


def delete_order():
    print("Delete an order")
    print("")   
    order_no = input("Please input your order number that you want to delete: ")
    order_no = order_no.strip()
    if not str.isdigit(order_no):
        print("order_no are integers")
        return
    order = get_order_by_id(order_no)
    print(f"Get an order that you want to delete {order}")
    
    delete_confirm = input("Are you sure to delete it (y/n): ")
    if delete_confirm.upper() != "Y":
        return

    if order == []:
        print("There is no such order,Please enter a new order!")
        return
    res = requests.delete(url(f"/order/{order_no}"))
    if res.status_code != 200:
        return
    elif res.status_code == 200:
        print("Delete successful!")
    
def get_order_by_customerId(customerId:int):
    res = requests.get(url(f"/order/customer/{customerId}"))
    if res.status_code != 200:
        return []   
    return res.json()

def get_my_orders():
    current_login = get_current_login()
    if current_login == []:
        print("You haven't login. Plese login first!")
        return
    for customer in current_login:
        customer_info =  Customer(**customer)

    customerId = customer_info.customerId
    my_orders = get_order_by_customerId(customerId)
    print("My orders!")
    for order in my_orders:
        order = Order_view(**order)
        print(f"Order No: {order.orderNo} Customer: {order.customer} ISBN:{order.ISBN} Quantity:{order.quantity} Price: {order.salesPrice} Order Date: {order.salesDate}") 

    
def update_book():
    pass

       