// background.js

// Обработчик сообщений от content.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'collectData') {
    // Отправляем данные о курсе на backend
    fetch('http://localhost:3000/add_course', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(message.data)
    })
    .then(response => response.json())
    .then(data => {
      console.log('Ответ от backend:', data);
    })
    .catch(error => {
      console.error('Ошибка при отправке данных:', error);
    });
  } else if (message.action === 'collectCatalogData') {
    // Отправляем данные о каталоге на backend
    message.data.forEach(course => {
      fetch('http://localhost:3000/add_course', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(course)
      })
      .then(response => response.json())
      .then(data => {
        console.log('Ответ от backend:', data);
      })
      .catch(error => {
        console.error('Ошибка при отправке данных:', error);
      });
    });
  }
});