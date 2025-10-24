import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1011",   # your MySQL root password or leave empty
            database="hospital_db"
        )
        return conn
    except Error as e:
        messagebox.showerror("Database Error", f"Connection failed:\n{e}")
        return None
