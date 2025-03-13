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
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            desc TEXT,
            site TEXT,
            price FLOAT,
            rating FLOAT,
            year INT,
            valuate TEXT
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def add_course_to_db(course_data: dict) -> int:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        INSERT INTO courses (name, desc, site, price, rating, year, valuate)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        course_data['name'], course_data['desc'], course_data['site'],
        course_data['price'], course_data['rating'], course_data['year'],
        course_data['valuate']
    ))
    course_id = cursor.fetchone()['id']
    conn.commit()
    cursor.close()
    conn.close()
    return course_id

if __name__ == "__main__":
    init_db()