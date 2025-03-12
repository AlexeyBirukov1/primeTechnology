chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "parseCourse") {
    const url = message.url;
    const headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    };

    fetch(url, { headers })
      .then(response => {
        if (!response.ok) {
          throw new Error(`Ошибка при загрузке страницы: ${response.status}`);
        }
        return response.text();
      })
      .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");

        // Извлекаем JSON-LD из тега <script>
        const jsonLdScript = doc.querySelector('script[type="application/ld+json"]');
        let courseData = {};
        if (jsonLdScript) {
          const jsonData = JSON.parse(jsonLdScript.textContent);

          courseData = {
            title: jsonData.name || "Название курса не найдено",
            description: jsonData.description || "Описание не найдено",
            price: parseFloat(jsonData.offers?.price) || 0,
            priceCurrency: jsonData.offers?.priceCurrency || "USD",
            rating: parseFloat(jsonData.aggregateRating?.ratingValue) || 0,
            ratingCount: parseInt(jsonData.aggregateRating?.ratingCount) || 0,
            url: jsonData.url || url
          };
        } else {
          // Fallback на старые селекторы, если JSON-LD нет
          courseData = {
            title: getText(doc, "h1.course-promo__header", "Название курса не найдено"),
            description: getText(doc, "div.course-promo__description", "Описание не найдено"),
            price: 0, // Нет данных в статике
            priceCurrency: "USD",
            rating: 0, // Нет данных в статике
            ratingCount: 0,
            url: url
          };
        }

        // Пока данных о сложности и уроках нет, добавим placeholders
        courseData.difficulty = "Сложность не найдена"; // Нужно уточнить селектор
        courseData.lessonsCount = "Количество уроков не указано"; // Нужно уточнить селектор

        // Логика сортировки (пример для одного курса, расширяемо для массива)
        const sortedCourseData = {
          ...courseData,
          // Здесь можно добавить сортировку, если будет массив курсов
          // Например, sortedCourses.sort((a, b) => a.price - b.price);
        };

        console.log("Данные курса:", sortedCourseData);
        sendResponse(sortedCourseData);
      })
      .catch(error => {
        console.error("Ошибка:", error);
        sendResponse({
          title: "Ошибка",
          description: `Не удалось загрузить страницу: ${error.message}`
        });
      });

    return true; // Асинхронный ответ
  }
});

// Вспомогательная функция для извлечения текста
function getText(doc, selector, defaultValue) {
  const element = doc.querySelector(selector);
  return element ? element.textContent.trim() : defaultValue;
}