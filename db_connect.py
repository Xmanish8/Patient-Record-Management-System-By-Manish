import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1011",  # Replace with your actual password
        database="hospital_db"
    )
