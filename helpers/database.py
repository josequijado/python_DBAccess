import mysql.connector as dbc
connection = dbc.connect()

class DBAccess:
    def __init__(self, host = "localhost", user = "root", password = ""):
        self.host = host
        self.user = user
        self.password = password
        self.connection = None  # Inicializar la conexión como None en el constructor
    
    def create_connection(self):
        connection = dbc.connect(
            host = self.host, 
            user = self.user, 
            password = self.password
        )
        self.connection = connection
    
    def create_cursor(self):
        if not self.connection:
            self.create_connection()
        self.cursor = self.connection.cursor()
           
    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
            del self.cursor
            del self.connection
            return True
        except Exception as e:
            return (False, e)
        
    def show_databases(self):
        self.cursor.execute("show databases")
        bases = [base[0] for base in self.cursor.fetchall()]
        return bases

    def select_database(self, database):
        self.database = database
        self.cursor.execute(f"create database if not exists {self.database}")
        self.cursor.execute(f"use {self.database}")
        self.connection.commit()

    def show_user_grants(self):
        self.cursor.execute("SHOW GRANTS")
        grants = [grant[0] for grant in self.cursor.fetchall()]
        return grants

    def get_tables(self):
        self.cursor.execute(f"show full tables from {self.database}")
        tables = [table[0] for table in self.cursor.fetchall()]
        return tables
    
    def get_data(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            data = [rec for rec in self.cursor.fetchall()]
        except Exception as e:
            data = False
        return data    
    
    def set_data(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            result = [True]
        except Exception as e:
            self.connection.rollback()
            result = [False, e]
        return result
