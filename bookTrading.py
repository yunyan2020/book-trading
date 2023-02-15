import requests
from api import User


def url(route: str):
    return f"http://127.0.0.1:8000{route}"

def get_all_users():
     users = []
     res = requests.get(url("/users"))
     if res.status_code != 200:
        return []
     for user in  res.json(): 
        user = User(**user) 
        print("_________________")
        print(f"ID: {user.id}")
        print(f"username: {user.username}")
        print(f"password: {user.password}")
        users.append(user)
     return users

def hasSameUsernameFunction(username:str):  
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

def getCredientials(username:str):
    res = requests.get(url(f"/user/{username.strip()}"))   
    if not res.status_code == 200:
         return    
    return res.json()

def saveLoinInfo(user:User):
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
    credientials =getCredientials(username)[0]
    stored_user = User(**credientials)   
    user = User(username=username, password=password)
    if username == stored_user.username and password == stored_user.password:
        logoutExistedUser()
        saveLoinInfo(user)
    else:
        print("Bad credentials")
