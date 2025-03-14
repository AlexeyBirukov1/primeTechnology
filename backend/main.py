from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .db import add_course_to_db, DB_FILE, init_db, get_best_course
from .gptanalysis import calculate_rating, get_data_from_db
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
    theme: str = "Не определена"
    description: str
    price: str = "0"
    rating: str
    reviews: str
    difficulty: str
    valuate: str = "0"
    link: str = "https://stepik.org/catalog"

class BestCourseRequest(BaseModel):
    min_price: int
    max_price: int
    difficulties: List[str]

def check_course_exists(course_name: str) -> bool:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM courses WHERE name = ?", (course_name,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

@app.post("/add_course")
async def add_course(course: Course):
    course_data = course.dict()
    if course_data['name'] == "Нет названия":
        return {"message": f"Курс не добавлен; Пустой запрос."}
    if check_course_exists(course_data['name']):
        return {"message": f"Курс '{course.name}' уже существует в базе."}
    course_id = add_course_to_db(course_data)

    course_data_db = get_data_from_db(course_id)
    if course_data_db:
        rating, theme, level = calculate_rating(course_data_db)
        if rating is not None:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("UPDATE courses SET valuate = ?, theme = ?, difficulty = ? WHERE id = ?",
                           (str(rating), str(theme), str(level), course_id))
            conn.commit()
            conn.close()
            return {
                "message": f"Курс {course.name} добавлен с ID {course_id}",
                "rating": rating,
                "theme": theme,
                "level": level
            }
    return {"message": f"Курс {course.name} добавлен с ID {course_id}", "rating": "Не удалось оценить"}

@app.get("/courses")
async def get_all_courses():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return [dict(course) for course in courses]

@app.post("/get_recommended_course")
async def get_recommended_course(request: BestCourseRequest):
    logger.info(f"Received request: min_price={request.min_price}, max_price={request.max_price}, difficulties={request.difficulties}")
    result = get_best_course(request.min_price, request.max_price, request.difficulties)
    if result:
        logger.info(f"Found course: {result}")
        return {
            "recommendedCourse": {
                "title": result["name"],
                "description": result["description"],
                "price": result["price"],
                "rating": result["rating"],
                "neuralRating": result["valuate"],
                "link": result["link"]
            }
        }
    logger.warning("No course found matching the criteria")
    raise HTTPException(status_code=404, detail={"message": "Рекомендуемый курс не найден"})

@app.get("/get_course_evaluation")
async def get_course_evaluation(link: str):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT valuate FROM courses WHERE link = ?", (link,))
    result = cursor.fetchone()
    conn.close()
    logger.info(f"Ошибка обработки данных курса: {result}")
    if result:
        return {"currentCourseRating": str(result["valuate"])}
    raise HTTPException(status_code=404, detail={"message": "Курс не найден в базе"})