import openai

API_KEY = ""  # Вставьте ваш ключ API
openai.api_key = API_KEY

def create_prompt(name, description, price, rating, reviews, difficulty, valuate):
    prompt = f"""
    Оцените курс на основе следующих параметров:
    - Название: {name}
    - Описание: {description}
    - Цена: {price}
    - Рейтинг: {rating}
    - Отзывы: {reviews}
    - Сложность: {difficulty}
    - Текущая оценка (если есть): {valuate if valuate else 'Не указана'}

    Проанализируйте тематику курса на основе названия и описания, определите, что это за тематика (например, "Программирование на Python").  
    Также определите уровень курса (начальный, средний или продвинутый) на основе описания и сложности.  
    Дайте общую оценку от 0 до 100, основываясь на качестве названия, описания, разумности цены, 
    рейтинга, количества отзывов, сложности и тематики проекта.  
    В ответе укажите:
    1. Числовую оценку (от 0 до 100).
    2. Тематику проекта (например, "Python").
    3. Уровень курса (начальный, средний или продвинутый) с кратким объяснением.
    """
    return prompt

def get_rating_from_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты помощник, который оценивает курсы и предоставляет числовую оценку от 0 до 100 с пояснениями."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        full_response = response.choices[0].message['content'].strip()

        lines = full_response.split('\n')
        if len(lines) < 3:
            raise ValueError("Ответ модели не содержит всех требуемых частей")

        rating = float(lines[0].strip())
        if not 0 <= rating <= 100:
            raise ValueError("Оценка должна быть в диапазоне от 0 до 100")

        theme = lines[1].strip()
        level = '\n'.join(lines[2:]).strip()

        return rating, theme, level

    except openai.error.OpenAIError as e:
        print(f"Ошибка API OpenAI: {e}")
        return None, None, None
    except ValueError as e:
        print(f"Ошибка обработки ответа: {e}")
        return None, None, None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None, None, None

def analyze_course(course_data):
    name, description, price, rating, reviews, difficulty, valuate = course_data
    prompt = create_prompt(name, description, price, rating, reviews, difficulty, valuate)
    return get_rating_from_chatgpt(prompt)