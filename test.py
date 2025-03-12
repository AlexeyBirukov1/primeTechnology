import requests
from bs4 import BeautifulSoup

# Функция для определения, есть ли на странице курсы
def is_course_page(url):
    # Проверяем URL или другие признаки
    return "catalog" in url or "courses" in url

# Функция для сбора информации о курсах
def scrape_courses(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    courses = []

    # Пример: находим все элементы с классом 'course-card'
    for course in soup.find_all('div', class_='course-card'):
        title = course.find('h3').text.strip()  # Название курса
        price = course.find('span', class_='price').text.strip()  # Цена
        duration = course.find('span', class_='duration').text.strip()  # Длительность
        rating = course.find('span', class_='rating').text.strip()  # Рейтинг

        # Добавляем курс в список
        courses.append({
            'title': title,
            'price': price,
            'duration': duration,
            'rating': rating
        })

    return courses

# Функция для отправки данных на API
def send_to_api(courses):
    api_url = "https://your-api.com/endpoint"
    response = requests.post(api_url, json=courses)
    if response.status_code == 200:
        print("Данные успешно отправлены на API!")
    else:
        print("Ошибка при отправке данных:", response.status_code)

# Основной код
if __name__ == "__main__":
    # Пример URL страницы с курсами
    url = "https://stepik.org/catalog"
    response = requests.get(url)

    if is_course_page(url):
        print("Это страница с курсами, начинаем парсинг...")
        courses = scrape_courses(response.text)
        print(f"Найдено курсов: {len(courses)}")
        send_to_api(courses)
    else:
        print("Это не страница с курсами.")