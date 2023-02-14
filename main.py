from bookTrading import register,get_all_users


def admin_session():
    while 1 :
        print("")
        print("Admin Menu")
        print("0. Get all users")
        print("1. Modify order")
        print("2. delete orders")
        print("3. Add a book") 
        print("4. Get all orders")      
        print("5. logout")  

        user_option = input(str("Option : "))
       
        if not str.isdigit(user_option):
            print("Please enter a valid option")
            return
               
        if user_option == "0":
            get_all_users()
        elif user_option == "1":
            print("Modify order")
        elif user_option == "2":    
            print("delete orders")
        elif user_option == "3":
            print("Add a book") 
        elif user_option == "4":
            print("Get all orders")  
        elif user_option == "5":
            break
        else:
            print("No valid option was selected")
           

def customer_session():
    while 1 :
        print("")
        print("Customer Menu")
        print("1. Register")
        print("2. Login")
        print("3. Shopping")
        print("4. Get my orders")
        print("5. logout")
        user_option = input(str("Option : "))
        if user_option == "1":
            register()
        elif user_option == "2":
            login()
        elif user_option == "3":
            print("Shopping")
        elif user_option == "4":
            print("Get my orders")
        elif user_option == "5":
            break
        else:
            print("No valid option was selected")
        
              

def auth_admin():
    print("")
    print("Admin Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    if username == "admin":
        if password == "admin123":
            admin_session()
        else:
            print("Incorrect password !")
    else:
      print("Login details not recognised")


def main_menu():
    while True:
        print("*************************************")
        print("Wellcome to the book trading system")
        print("")
        print("1. Customer Option")
        print("2. Login as admin")
        print("3. Exit")
        print("*************************************")
        print("")
        user_option = input(str("Option : "))
        if user_option == "1":
            customer_session()
        elif user_option == "2":
            auth_admin()
        elif user_option == "3":
            break
        else:
            print("No valid option was selected")


main_menu()
