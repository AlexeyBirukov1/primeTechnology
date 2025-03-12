chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "parseCourse") {
    const url = message.url;

    // Отправляем запрос на сервер
    fetch(`http://127.0.0.1:8000/parse-course?url=${encodeURIComponent(url)}`)
      .then(response => response.json())
      .then(data => {
        sendResponse(data);
      })
      .catch(error => {
        console.error("Ошибка:", error);
        sendResponse({
          title: "Ошибка",
          description: "Не удалось связаться с сервером"
        });
      });

    // Возвращаем true для асинхронного ответа
    return true;
  }
});