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
            theme TEXT,
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

def add_course_to_db(course_data: Dict) -> int:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO courses (name, theme, description, price, rating, reviews, difficulty, valuate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        course_data['name'],
        course_data.get('theme', 'Не определена'),
        course_data['description'],
        course_data['price'],
        course_data['rating'],
        course_data['reviews'],
        course_data['difficulty'],
        course_data.get('valuate', '0')  # Значение по умолчанию
    ))
    course_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return course_id

if __name__ == "__main__":
    init_db()