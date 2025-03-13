from fastapi import FastAPI
from pydantic import BaseModel
from .db import add_course_to_db, DB_FILE, init_db
import sqlite3
import logging
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


class Course(BaseModel):
    name: str
    description: str
    price: str
    rating: str
    reviews: str
    difficulty: str
    valuate: str


@app.post("/add_course")
async def add_course_endpoint(course: Course):
    course_data = course.dict()
    course_id = add_course_to_db(course_data)

    # Получаем данные курса из БД
    course_data_db = get_course_data(course_id)
    # Анализируем курс через GPT
    rating, theme, level = analyze_course(course_data_db)

    # Обновляем поле valuate в базе данных
    if rating is not None:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE courses SET valuate = ? WHERE id = ?", (f"{rating}/100", course_id))
        conn.commit()
        conn.close()

    return {
        "message": f"Курс {course.name} добавлен с ID {course_id}",
        "rating": rating,
        "theme": theme,
        "level": level
    }


@app.get("/courses")
async def get_all_courses():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return [dict(course) for course in courses]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)