import pyodbc

db_server = "localhost\SQLEXPRESS"
# db_server = "LAPTOP-800N131K\SQLEXPRESS"
db_name = "bookTrading2"
db_driver = "ODBC Driver 17 for SQL Server"

connection_string = f"""
DRIVER={db_driver};
SERVER={db_server};
DATABASE={db_name};
trusted_connection=yes;
"""


class DB:    
    def call_db(self, query, *args):
        data = None
        conn = pyodbc.connect(connection_string)
        cur  = conn.cursor()
        if "SELECT" in query:     
            print(f"Executing query: {query} with parameters: {args}")       
            res = cur.execute(query, args)                 
            data = res.fetchall()
            print(f"Result of query execution: {data}")  
            cur.close()
        else:
            conn.execute(query,args)
            print(f"Executing query1: {query} with parameters: {args}")  
        conn.commit()
        conn.close()
        return data