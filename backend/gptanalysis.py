import sqlite3
import openai


API_KEY = ""  # как дадут ключ вставим


openai.api_key = API_KEY

def get_data_from_db():
    try:
        conn = sqlite3.connect('.db')  # ТУТ НУЖНО НАЗВАНИЕ БД
        cursor = conn.cursor()

        # ИЗМЕНИТ ПОД БД
        cursor.execute("SELECT имя, описание, сайт, цена, рейтинг, год, оценка FROM items LIMIT 1")
        data = cursor.fetchone()

        if data is None:
            raise ValueError("Нет данных в базе данных")

        name, description, site, price, rating, year, existing_rating = data

        if not all([name, description, site, price is not None, rating is not None, year is not None]):
            raise ValueError("Одно или несколько обязательных полей отсутствуют или пустые")
        if not isinstance(price, int) or not isinstance(rating, int) or not isinstance(year, int):
            raise ValueError("Цена, рейтинг и год должны быть целыми числами")
        if price < 0 or rating < 0 or year < 1900 or year > 2025:
            raise ValueError("Некорректные значения для цены, рейтинга или года")

        conn.close()
        return name, description, site, price, rating, year, existing_rating

    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None
    except ValueError as e:
        print(f"Ошибка данных: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None


def create_prompt(name, description, site, price, rating, year, existing_rating):
    prompt = f"""
    Оцените объект на основе следующих параметров:
    - Имя: {name}
    - Описание: {description}
    - Сайт: {site}
    - Цена: {price}
    - Рейтинг: {rating}
    - Год: {year}
    - Текущая оценка (если есть): {existing_rating if existing_rating else 'Не указана'}

    Пожалуйста, дайте общую оценку от 0 до 100, основываясь на качестве имени, описания, релевантности сайта, разумности цены, рейтинга и актуальности года. Оценка должна быть числом без дополнительных комментариев.
    """
    return prompt


def get_rating_from_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты помощник, который дает числовую оценку от 0 до 100."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0.7
        )
        rating = response.choices[0].message['content'].strip()

        rating = float(rating)
        if not 0 <= rating <= 100:
            raise ValueError("Оценка должна быть в диапазоне от 0 до 100")

        return rating

    except openai.error.OpenAIError as e:
        print(f"Ошибка API OpenAI: {e}")
        return None
    except ValueError as e:
        print(f"Ошибка обработки ответа: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None

def analyze_course():
    data = get_data_from_db()
    if data is None:
        return None

    name, description, site, price, rating, year, existing_rating = data
    prompt = create_prompt(name, description, site, price, rating, year, existing_rating)
    rating = get_rating_from_chatgpt(prompt)
    return rating

if __name__ == "__main__":
    final_rating = analyze_course()
    if final_rating is not None:
        print(final_rating)  # оценка
    else:
        print("Не удалось получить оценку")
