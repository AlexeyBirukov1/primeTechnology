document.addEventListener('DOMContentLoaded', () => {
    // Получаем данные с активной вкладки
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            function: extractCourseData
        }, (results) => {
            const courseData = results[0].result || {
                name: "Не найдено",
                desc: "Не найдено",
                site: "Не найдено",
                price: 0,
                rating: 0,
                year: 2025, // Заглушка, т.к. года нет в HTML
                valuate: "Пока нет оценки"
            };

            // Заполняем поля в popup
            document.getElementById('name').textContent = courseData.name;
            document.getElementById('desc').textContent = courseData.desc;
            document.getElementById('site').textContent = courseData.site;
            document.getElementById('price').textContent = courseData.price;
            document.getElementById('rating').textContent = courseData.rating;
            document.getElementById('year').textContent = courseData.year;
            document.getElementById('valuate').textContent = courseData.valuate;

            // Отправка на бэкенд
            document.getElementById('send-btn').addEventListener('click', () => {
                fetch('http://localhost:8000/add_course', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(courseData)
                })
                .then(response => response.json())
                .then(data => alert('Курс добавлен: ' + data.message))
                .catch(error => alert('Ошибка: ' + error));
            });
        });
    });
});

// Функция для извлечения данных из карточки курса
function extractCourseData() {
    const card = document.querySelector('.course-card');
    if (!card) return null;

    // Название курса
    const name = card.querySelector('.course-card__title')?.textContent.trim() || "Не указано";

    // Описание курса
    const desc = card.querySelector('.course-card__summary .shortened-text')?.textContent.trim() || "Не указано";

    // Ссылка на курс (добавляем базовый домен, если нужно)
    const siteRelative = card.querySelector('.catalog-rich-card__link-wrapper')?.getAttribute('href') || "";
    const site = siteRelative ? `https://stepik.org${siteRelative}` : "Не указано";

    const priceRegular = card.querySelector('.display-price__price_regular')?.textContent || "";
    const priceText = priceDiscount || priceRegular || "0";
    const price = parseFloat(priceText.replace(/[^\d]/g, '')) || 0;

    // Рейтинг (берем число из текста, например, "5 (1.4K)")
    const ratingText = card.querySelector('.course-card__widget[data-type="rating"] > span:last-child')?.textContent || "0";
    const rating = parseFloat(ratingText.split(' ')[0]) || 0;

    const year = 2025; // Можно заменить, если найдёте источник

    return {
        name: name,
        desc: desc,
        site: site,
        price: price,
        rating: rating,
        year: year,
        valuate: "Пока нет оценки"
    };
}