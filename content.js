// content.js

// Функция для сбора данных о курсе
function collectCourseData() {
    const courseTitle = document.querySelector('h1')?.innerText.trim() || 'Нет названия';
    const courseDescription = document.querySelector('meta[name="description"]')?.content || 'Нет описания';
    const coursePrice = document.querySelector('.price')?.innerText.trim() || 'Бесплатно';
    const ratingStars = document.querySelector('.rating')?.innerText.trim() || 'Нет рейтинга';
    const reviewsCount = document.querySelector('.reviews')?.innerText.trim() || 'Нет отзывов';
  
    return {
      title: courseTitle,
      description: courseDescription,
      price: coursePrice,
      rating: ratingStars,
      reviews: reviewsCount
    };
  }
  
  // Обработчик сообщений от popup.js
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'collectCourseData') {
      const courseData = collectCourseData();
      sendResponse({ data: courseData });
    }
  });