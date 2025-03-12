import requests
from bs4 import BeautifulSoup

# URL ����� �� Stepik (������ �� ����)
url = "https://stepik.org/course/58852"

# ���������, ����� ���� �� ���������� ������
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# ��������� ������ � ��������
response = requests.get(url, headers=headers)

# ���������, ��� ������ �������
if response.status_code == 200:
    # ������ HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # ��������� �������� ����� (������ � ���� <h1> � �������)
    title = soup.find("h1", class_="course-promo__header")
    if title:
        print("�������� �����:", title.text.strip())
    else:
        print("�������� ����� �� �������")

    # ��������� �������� ����� (����� ���� � ���� <div> � ������������ �������)
    description = soup.find("div", class_="course-promo__description")
    if description:
        print("��������:", description.text.strip())
    else:
        print("�������� �� �������")

else:
    print(f"������ ��� �������� ��������: {response.status_code}")