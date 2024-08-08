import os

import sqlite3 
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

def get_db_connection():
    conn = sqlite3.connect('birthdays.db') # creates a connect to the data base 
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS birthdays (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     month INTEGER NOT NULL,
                     day INTEGER NOT NULL 
                     )
                     ''')
    conn.close() 

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    init_db()
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")  
        db = get_db_connection()
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", (name, month, day))
        db.commit()
        db.close()

        return redirect("/")
    else:
        name = ""
        month = ""
        day = ""
        conn = get_db_connection()
        birthdays = conn.execute("SELECT * FROM birthdays").fetchall()
        conn.close()
        return render_template("index.html", name=name, month=month, day=day, birthdays=birthdays)
    