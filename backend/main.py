from fastapi import FastAPI
from pydantic import BaseModel
from .db import add_course_to_db
from .gptanalysis import analyze_course  # Теперь импортируем из пакета backend

app = FastAPI()

class Course(BaseModel):
    name: str
    description: str
    price: float
    rating: float
    reviews: int
    difficulty: str
    valuate: str

@app.post("/add_course")
async def add_course(course: Course):
    # Анализ курса через GPT (раскомментируй, когда будет готово)
    # valuate = analyze_course() or "12/10"  # Заглушка, если GPT не работает
    valuate = None
    course_data = course.dict()
    course_data['valuate'] = valuate

    # Добавление в базу
    course_id = add_course_to_db(course_data)
    return {"message": f"Курс {course.name} добавлен с ID {course_id}"}