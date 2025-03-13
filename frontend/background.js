chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log(message.data);
  if (message.action === 'collectData') {
    fetch('http://127.0.0.1:8000/add_course', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(message.data)
    })
    .then(response => response.json())
    .then(data => {
      console.log('Ответ от backend:', data);
      sendResponse({ success: true, data });
    })
    .catch(error => {
      console.error('Ошибка:', error);
      sendResponse({ success: false, error });
    });
    return true;
  } else if (message.action === 'applyFilters') {
    console.log('Фильтры:', message.filters);
    sendResponse({ success: true, message: 'Фильтры получены' });
    return true;
  } else if (message.action === 'evaluateCourse') {
    fetch('http://127.0.0.1:8000/add_course', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(message.data)
    })
    .then(response => response.json())
    .then(data => {
      sendResponse({
        success: true,
        courseRating: data.rating || '80',  // Значение по умолчанию, если рейтинг не вернулся
        recommendedCourse: message.data
      });
    })
    .catch(error => {
      sendResponse({ success: false, error });
    });
    return true;
  }
});