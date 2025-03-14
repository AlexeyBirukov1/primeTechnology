import logging
import sqlite3
from typing import Dict, Optional
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


def get_theme_by_name(course_name: str) -> Optional[str]:
    """
    Возвращает тему курса по его названию.

    Args:
        course_name (str): Название курса для поиска.

    Returns:
        Optional[str]: Значение поля theme или None, если курс не найден.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT theme FROM courses WHERE name = ?", (course_name,))
    result = cursor.fetchone()

    conn.close()

    return result["theme"] if result else None

def get_best_course(min_price: int, max_price: int, difficulties: list, catalog_theme:str) -> dict:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT name, description, rating, price, valuate, link
        FROM courses
        WHERE price BETWEEN ? AND ?
          AND difficulty IN ({})
          AND theme = ?
        ORDER BY valuate DESC
        LIMIT 1;
    """.format(", ".join("?" * len(difficulties)))

    cursor.execute(query, (min_price, max_price, *difficulties, catalog_theme))
    result = cursor.fetchone()
    conn.close()
    logger.info(f"По запросу {min_price, max_price, difficulties, catalog_theme}, найдено было: {result}")
    if result:
        return dict(result)
    return None

if __name__ == "__main__":
    init_db()