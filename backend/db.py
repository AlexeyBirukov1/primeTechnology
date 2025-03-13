import sqlite3
from typing import Dict

DB_FILE = "courses.sqlite"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price TEXT,
            rating TEXT,
            reviews TEXT,
            difficulty TEXT,
            valuate TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def add_course_to_db(course_data: dict) -> int:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO courses (name, description, price, rating, reviews, difficulty, valuate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
        course_data['name'],
        course_data['description'],
        course_data['price'],
        course_data['rating'],
        course_data['reviews'],
        course_data['difficulty'],
        course_data['valuate']
    ))
    course_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return course_id

def get_course_data(course_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, price, rating, reviews, difficulty, valuate FROM courses WHERE id = ?", (course_id,))
    data = cursor.fetchone()
    conn.close()
    return data