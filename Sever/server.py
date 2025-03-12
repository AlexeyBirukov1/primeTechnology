from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники (для теста)
    allow_methods=["*"],  # Разрешаем все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

def parse_course_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        title = soup.find("h1", class_="course-promo__header")
        title_text = title.text.strip() if title else "Название курса не найдено"
        
        description = soup.find("div", class_="course-promo__description")
        description_text = description.text.strip() if description else "Описание не найдено"
        
        return {
            "title": title_text,
            "description": description_text
        }
    else:
        return {
            "title": "Ошибка",
            "description": f"Не удалось загрузить страницу: {response.status_code}"
        }

@app.get("/parse-course")
async def get_course_data(url: str):
    data = parse_course_data(url)
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)