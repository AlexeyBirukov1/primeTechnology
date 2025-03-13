chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'evaluateCourse') {
    console.log('Получены данные для отправки:', message.data);
    fetch('http://127.0.0.1:8000/add_course', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(message.data)
    })
    .then(response => {
      console.log('Статус ответа сервера:', response.status);
      if (!response.ok) throw new Error(`Ошибка: ${response.status}`);
      return response.json();
    })
    .then(data => {
      console.log('Ответ от сервера:', data);
      sendResponse(data);
    })
    .catch(error => {
      console.error('Ошибка:', error);
      sendResponse({ error: error.message });
    });
    return true;
  }
});