import logging
import sqlite3
from typing import Dict
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            price INT,
            rating FLOAT,
            reviews INT,
            difficulty TEXT,
            valuate INT,
            link TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def add_course_to_db(course_data: Dict) -> int:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        price = int("".join(re.findall(r"\d+", course_data['price'])))
        rating_match = re.search(r"\d+\.?\d*", course_data['rating'])
        rating = float(rating_match.group()) if rating_match else 0.0
        reviews = int("".join(re.findall(r"\d+", course_data['reviews'])))
    except (ValueError, AttributeError) as e:
        logger.error(f"Ошибка обработки данных курса: {e}")
        price, rating, reviews = 0, 0.0, 0  # Значения по умолчанию
    cursor.execute("""
        INSERT INTO courses (name, theme, description, price, rating, reviews, difficulty, valuate, link)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        course_data['name'],
        course_data.get('theme', 'Не определена'),
        course_data['description'],
        price,
        rating,
        reviews,
        course_data['difficulty'],
        course_data.get('valuate', '0'),
        course_data['link']
    ))
    course_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return course_id

def get_best_course(min_price: int, max_price: int, difficulties: list) -> dict:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT name, description, rating, price, valuate, link
        FROM courses
        WHERE price BETWEEN ? AND ?
          AND difficulty IN ({})
        ORDER BY valuate DESC
        LIMIT 1;
    """.format(", ".join("?" * len(difficulties)))

    cursor.execute(query, (min_price, max_price, *difficulties))
    result = cursor.fetchone()
    conn.close()

    if result:
        return dict(result)
    return None

if __name__ == "__main__":
    init_db()