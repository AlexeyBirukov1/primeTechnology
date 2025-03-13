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
    allow_origins=["*"],  # Разрешить все источники (для тестов) или укажите "chrome-extension://<your-extension-id>"
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
async def add_course(course: Course):
    # Анализ курса через GPT (раскомментируй, когда будет готово)
    # valuate = analyze_course() or "12/10"  # Заглушка, если GPT не работает
    valuate = None
    course_data = course.dict()
    # Поле 'valuate' пока оставляем как None, если GPT не используется
    course_data['valuate'] = valuate
    logger.info(course_data)
    # Добавление в базу
    course_id = add_course_to_db(course_data)
    return {"message": f"Курс {course.name} добавлен с ID {course_id}"}

# Новый эндпоинт для получения всех курсов
@app.get("/courses")
async def get_all_courses():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Позволяет получать данные как словари
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return [dict(course) for course in courses]