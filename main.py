from bookTrading import register,get_all_users,login,logoutExistedUser,import_book_csv_data
from bookTrading import import_authors_csv_data,order_books,change_password,delete_order,get_my_orders,update_book

def admin_session():
    while 1 :
        print("")
        print("Admin Menu")
        print("0. Get all users")
        print("1. Import authors") 
        print("2. Import books")
        print("3. Delete an order") 
        print("4. Update book's titile and price ")    
        print("5. Exit")  

        user_option = input(str("Option : "))
       
        if not str.isdigit(user_option):
            print("Please enter a valid option")
            return
               
        if user_option == "0":
            get_all_users()
        elif user_option == "1":
            import_authors_csv_data()             
        elif user_option == "2":   
            import_book_csv_data()   
        elif user_option == "3":
            delete_order() 
        elif user_option == "4":
            update_book()   
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
        print("3. Order books")
        print("4. Change password")
        print("5. Get my orders")
        print("6. logout")
        print("7. Exit without logout")
        user_option = input(str("Option : "))
        if user_option == "1":
            register()
        elif user_option == "2":
            login()
        elif user_option == "3":
            order_books()
        elif user_option == "4":
            change_password()
        elif user_option == "5":
            get_my_orders()
        elif user_option == "6":
            logoutExistedUser()
            print("Logout successful")  
            break
        elif user_option == "7":
            print("Exit without logout")  
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
