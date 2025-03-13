import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "courses_db",
    "user": "postgres",
    "password": "COMBO",
    "host": "localhost",
    "port": "5432"
}

def init_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Удаляем старую таблицу, если она есть
        # Создаём новую таблицу с актуальной структурой
        cursor.execute("""
            CREATE TABLE courses (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price FLOAT,
                rating FLOAT,
                reviews INT,
                difficulty TEXT,
                valuate INT
            );
        """)
        conn.commit()
        print("Таблица courses создана успешно")
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        cursor.close()
        conn.close()

def add_course_to_db(course_data: dict) -> int:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            INSERT INTO courses (name, description, price, rating, reviews, difficulty, valuate)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            course_data['name'], course_data['description'], course_data['price'],
            course_data['rating'], course_data['reviews'], course_data['difficulty'],
            course_data['valuate']
        ))
        course_id = cursor.fetchone()['id']
        conn.commit()
        return course_id
    except Exception as e:
        print(f"Ошибка при добавлении курса: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def get_all_courses():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM courses;")
        rows = cursor.fetchall()
        if not rows:
            print("Таблица courses пуста")
        for row in rows:
            print(row)
            print("COCAL")
    except Exception as e:
        print(f"Ошибка при выборке данных: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_db()
    get_all_courses()