import mysql.connector


def connect_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="Sakshi@2005*", database="attendance_db"
    )