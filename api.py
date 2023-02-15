from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

# from db import DB
from mssql_db import DB


class User(BaseModel):
    id: int = None
    username: str
    password: str


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
    # users = []
    # for element in data:
    #     id,username,password  =element
    #     users.append(User(id=id,username=username,password=password))
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
    print(login_date)
    insert_query = """
    INSERT INTO currentLogin (username,password,loginDate)
    VALUES (?,?,?)
    """
    db.call_db(insert_query, user.username, user.password,login_date)
    return "Login a user"

@app.get("/user/{username}")
def get_user_by_username(username: str):
    print("parameter username ")
    print(username)
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
