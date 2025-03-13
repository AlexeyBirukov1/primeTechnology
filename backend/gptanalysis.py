import openai

API_KEY = ""  # Вставь ключ, когда будет
openai.api_key = API_KEY

def create_prompt(course_data: dict):
    prompt = f"""
    Оцените курс на основе следующих параметров:
    - Название: {course_data['name']}
    - Описание: {course_data['desc']}
    - Сайт: {course_data['site']}
    - Цена: {course_data['price']}
    - Рейтинг: {course_data['rating']}
    - Год: {course_data['year']}

    Дайте общую оценку от 0 до 100, основываясь на качестве названия, описания, релевантности сайта, разумности цены, рейтинга и актуальности года. Оценка должна быть числом без комментариев.
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
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def analyze_course(course_data: dict):
    prompt = create_prompt(course_data)
    rating = get_rating_from_chatgpt(prompt)
    return str(rating) if rating is not None else None

if __name__ == "__main__":
    # Тестовый пример
    test_data = {
        "name": "Test Course",
        "desc": "This is a test course",
        "site": "example.com",
        "price": 100.0,
        "rating": 4.5,
        "year": 2023
    }
    rating = analyze_course(test_data)
    print(rating)