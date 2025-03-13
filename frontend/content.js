// content.js

// Функция для сбора данных о курсе
function collectCourseData() {
  const courseTitle = document.querySelector('h1.course-title')?.innerText.trim() || 'Нет названия';
  const courseDescription = document.querySelector('div.course-summary')?.innerText.trim() || 'Нет описания';
  const coursePrice = document.querySelector('div.course-purchase-widget__price')?.innerText.trim() || 'Бесплатно';
  const ratingStars = document.querySelector('div.course-rating__stars')?.getAttribute('aria-label') || 'Нет рейтинга';
  const reviewsCount = document.querySelector('div.course-rating__reviews')?.innerText.trim() || 'Нет отзывов';
  const courseLevel = document.querySelector('div.course-sidebar__category')?.innerText.trim() || 'Неизвестно';

  return {
    title: courseTitle,
    description: courseDescription,
    price: coursePrice,
    rating: ratingStars,
    reviews: reviewsCount,
    level: courseLevel
  };
}

// Функция для сбора данных о курсах из каталога
function collectCatalogData() {
  const courses = [];
  document.querySelectorAll('div.course-card').forEach(card => {
    const title = card.querySelector('h3.course-card__title')?.innerText.trim() || 'Нет названия';
    const description = card.querySelector('div.course-card__description')?.innerText.trim() || 'Нет описания';
    const price = card.querySelector('div.course-card__price')?.innerText.trim() || 'Бесплатно';
    const rating = card.querySelector('div.course-card__rating')?.innerText.trim() || 'Нет рейтинга';
    const reviews = card.querySelector('div.course-card__reviews')?.innerText.trim() || 'Нет отзывов';
    const level = card.querySelector('div.course-card__level')?.innerText.trim() || 'Неизвестно';

    courses.push({
      title,
      description,
      price,
      rating,
      reviews,
      level
    });
  });

  return courses;
}

// Проверяем, находимся ли мы на странице курса или каталога
if (window.location.href.includes('/course/')) {
  // Если это страница курса, собираем данные
  const courseData = collectCourseData();
  chrome.runtime.sendMessage({ action: 'collectData', data: courseData });
} else if (window.location.href.includes('/catalog/')) {
  // Если это каталог, собираем данные о всех курсах
  const catalogData = collectCatalogData();
  chrome.runtime.sendMessage({ action: 'collectCatalogData', data: catalogData });
}