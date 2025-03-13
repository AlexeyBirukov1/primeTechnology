// background.js

// Обработчик сообщений от popup.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'evaluateCourse') {
    // Отправляем данные на backend
    fetch('http://127.0.0.1:8000/add_course', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(message.data)
    })
    .then(response => response.json())
    .then(data => {
      // Возвращаем оценку курса и данные рекомендуемого курса
      sendResponse(data);
    })
    .catch(error => {
      console.error('Ошибка при отправке данных:', error);
      sendResponse(null);
    });

    // Возвращаем true для асинхронного ответа
    return true;
  }
});