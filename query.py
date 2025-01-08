import mysql.connector
import streamlit as st

# Connection
conn = mysql.connector.connect(
    host = "localhost",
    port = "4306",
    user = "root",
    password = "",
    db = "ins_db"
)

c = conn.cursor()

# Fetch
def view_all_data():
    c.execute('select * from ins_data order by id asc')
    data = c.fetchall()
    return data


