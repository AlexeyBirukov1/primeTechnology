import logging
import sqlite3
from openai import OpenAI

API_KEY = ""  # Вставьте ключ OpenAI
client = OpenAI(api_key=API_KEY)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_FILE = "courses.sqlite"

def get_data_from_db(course_id=None):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        if course_id:
            cursor.execute("SELECT name, theme, description, price, rating, reviews, difficulty, valuate, link FROM courses WHERE id = ?", (course_id,))
        else:
            cursor.execute("SELECT name, theme, description, price, rating, reviews, difficulty, valuate, link FROM courses LIMIT 1")
        data = cursor.fetchone()
        conn.close()

        if data is None:
            raise ValueError("Нет данных в базе данных")

        name, theme, description, price, rating, reviews, difficulty, valuate, link = data
        return {
            "name": name,
            "description": description,
            "price": price,
            "rating": rating,
            "reviews": reviews,
            "difficulty": difficulty,
            "valuate": valuate,
            "link": link
        }

    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

def create_prompt(course_data):
    prompt = f"""
    Оцените курс на основе следующих параметров:
    - Название: {course_data['name']}
    - Описание: {course_data['description']}
    - Цена: {course_data['price']} ₽
    - Рейтинг: {course_data['rating']}
    - Количество отзывов: {course_data['reviews']}
    - Уровень сложности: {course_data['difficulty']}
    - Текущая оценка: {course_data['valuate'] if course_data['valuate'] else 'Не указана'}

     Проанализируйте тематику курса на основе названия и описания (например, "Программирование на Python").
    Определите уровень курса (начальный, средний, продвинутый) на основе описания и сложности.
    Дайте общую оценку от 0 до 100, учитывая качество названия, описания, разумность цены, рейтинг, 
    количество отзывов и сложность.
    В ответе укажите только и ничего больше: 
    1. Числовую оценку (от 0 до 100).
    2. Тематику курса в формате тега (1 слово, например, "Python") 
    3. Уровень курса (выберите из трех вариантов: начальный, средний или продвинутый).
    Ответ должен быть указан в формате рода "89, Python, Начальный"
    """
    return prompt

def get_rating_from_chatgpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты помощник, который оценивает курсы и предоставляет числовую оценку от 0 до 100 с пояснениями."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        full_response = response.choices[0].message.content.strip()
        logger.info(full_response)
        lines = full_response.split(', ')
        if len(lines) < 3:
            raise ValueError("Ответ модели не содержит всех требуемых частей")

        rating = float(lines[0].strip())
        theme = lines[1].strip()
        level = '\n'.join(lines[2:]).strip()
        return rating, theme, level

    except Exception as e:
        logger.error(f"Ошибка при обращении к OpenAI: {e}")
        return None, None, None

def calculate_rating(course_data):
    prompt = create_prompt(course_data)
    rating, theme, level = get_rating_from_chatgpt(prompt)
    return rating, theme, level

if __name__ == "__main__":
    course_data = get_data_from_db()
    if course_data:
        rating, theme, level = calculate_rating(course_data)
        if rating is not None:
            print(f"Оценка: {rating}")
            print(f"Тематика: {theme}")
            print(f"Уровень: {level}")
        else:
            print("Не удалось получить оценку")