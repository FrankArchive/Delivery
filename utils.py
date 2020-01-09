from config import config
import MySQLdb
from flask import render_template

def db_conn():
    return MySQLdb.connect(**config["database_creds"])

def db_cursor():
    conn = db_conn()
    return conn.cursor()

def db_execute(sql, *args):
    cur = db_cursor()
    cur.execute(sql, *args)
    return cur

def error_page(error_list):
    return render_template('error.html', errors=error_list)
