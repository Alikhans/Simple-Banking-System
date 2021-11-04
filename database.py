import sqlite3
from sqlite3.dbapi2 import Connection

CREATE_TABLE_card =  """CREATE TABLE IF NOT EXISTS card (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT,
        PIN TEXT,
        balance INTEGER DEFAULT 0);"""

INSERT_CARD = "INSERT INTO card (number, PIN) VALUES (?, ?);"

GET_ALL_INFO = "SELECT * FROM card;"

CHECK_CARD_BY_NUM = "SELECT * FROM card WHERE number = ? AND PIN = ?;"

INSERT_MONEY = "UPDATE card SET balance = balance + ? where number = ? and PIN = ?;"

GET_BALANCE = "SELECT * FROM card WHERE balance = ?;"

TRANS = "SELECT * FROM card WHERE number = ?;"

DELETE_ROW = "DELETE FROM card WHERE number = ?;"

SENDER = "UPDATE card SET balance = balance - ? WHERE number = ? and PIN = ?;"

RECIEVER = "UPDATE card SET balance = balance + ? WHERE number = ?;"

def connect():
    return sqlite3.connect("card.s3db")

def reciever(connection, balance, number):
    with connection:
        connection.execute(RECIEVER, (balance, number))

def delete_row(connection, number):
    with connection:
        connection.execute(DELETE_ROW, (number,))

def create_tables(connection):
    with connection:
        connection.execute(CREATE_TABLE_card)

def add_data(connection, number, PIN):
    with connection:
        connection.execute(INSERT_CARD, (number, PIN))


def get_all_info(connection):
    with connection:
        return connection.execute(GET_ALL_INFO).fetchall()


def get_balance(connection):
    with connection:
        return connection.execute(GET_BALANCE).fetchone()


def println(connection, number, PIN):
    with connection:
        return connection.execute(CHECK_CARD_BY_NUM,(number, PIN)).fetchall()   


def insert_money(connection, balance, num, pin):
    with connection:
        connection.execute(INSERT_MONEY, (balance, num, pin))               

def transac(conn, num):
    with conn:
        return conn.execute(TRANS,(num,)).fetchone()

def sender(connection, balance, number, PIN):
    with connection:
        connection.execute(SENDER, (balance, number, PIN))          

