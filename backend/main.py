from fastapi import FastAPI
from pydantic import BaseModel
from db import add_course_to_db
from gptanalysis import analyze_course

app = FastAPI()


class Course(BaseModel):
    name: str
    desc: str
    site: str
    price: float
    rating: float
    year: int
    valuate: str


@app.post("/add_course")
async def add_course(course: Course):
    # Анализ курса через заглушку GPT
    valuate = analyze_course(course.desc)
    course_data = course.   dict()
    course_data['valuate'] = valuate

    # Добавление в базу
    course_id = add_course_to_db(course_data)
    return {"message": f"Курс {course.name} добавлен с ID {course_id}"}