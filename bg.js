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
        // Парсим HTML с помощью DOMParser
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");

        // Извлекаем название курса
        const titleElement = doc.querySelector("h1.course-promo__header");
        const title = titleElement ? titleElement.textContent.trim() : "Название курса не найдено";

        // Извлекаем описание
        const descriptionElement = doc.querySelector("div.course-promo__description");
        const description = descriptionElement ? descriptionElement.textContent.trim() : "Описание не найдено";

        // Формируем результат
        const courseData = {
          title: title,
          description: description
        };

        console.log("Данные курса:", courseData);
        sendResponse(courseData);
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