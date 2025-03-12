import requests
from bs4 import BeautifulSoup

# URL курса на Stepik (замени на свой)
url = "https://stepik.org/course/58852"

# Заголовки, чтобы сайт не блокировал запрос
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Выполняем запрос к странице
response = requests.get(url, headers=headers)

# Проверяем, что запрос успешен
if response.status_code == 200:
    # Парсим HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Извлекаем название курса (обычно в теге <h1> с классом)
    title = soup.find("h1", class_="course-promo__header")
    if title:
        print("Название курса:", title.text.strip())
    else:
        print("Название курса не найдено")

    # Извлекаем описание курса (может быть в теге <div> с определенным классом)
    description = soup.find("div", class_="course-promo__description")
    if description:
        print("Описание:", description.text.strip())
    else:
        print("Описание не найдено")

else:
    print(f"Ошибка при загрузке страницы: {response.status_code}")