// content.js
// Функция для сбора данных о курсе
function collectCourseData() {
  const courseTitle = document.querySelector('h1.course-promo__header')?.innerText.trim() || 'Нет названия';
  const courseDescription = document.querySelector('p.course-promo__summary .shortened-text')?.innerText.trim() || 'Нет описания';

  const priceElement = document.querySelector('span.display-price__price');
  const coursePrice = priceElement ? priceElement.querySelector('.format-price')?.innerText.trim().replace('₽', '').replace(/\s/g, '') : '0.0';

  const ratingElement = document.querySelector('span.course-promo-summary__average');
  const ratingStars = ratingElement ? ratingElement.innerText.trim() : '0.0';

  const reviewsElement = document.querySelector('a.course-promo-summary__reviews-count');
  const courseReviews = reviewsElement ? reviewsElement.innerText.trim().match(/\d+/g)?.join('') || '0' : '0';

  const levelElement = document.querySelector('div.course-promo__head-widget[data-type="difficulty"]');
  const courseLevel = levelElement ? levelElement.textContent.trim().replace(levelElement.querySelector('span')?.textContent.trim() || '', '').trim() : 'Неизвестно';

  const courseVal = "0"
  return {
    name: courseTitle,
    description: courseDescription,
    price: coursePrice,
    rating: ratingStars,
    reviews: courseReviews,
    difficulty: courseLevel,
    valuate: courseVal
  };
}

// Функция для сбора данных о курсах из каталога
function collectCatalogData() {
  console.log('content.js загружен');
  let courses = [];
  document.querySelectorAll('div.course-card').forEach(card => {
    const catalogTitle = card.querySelector('a.course-card__title')?.innerText.trim() || 'Нет названия';
    const catalogDescription = card.querySelector('span.course-card__summary .shortened-text')?.innerText.trim() || 'Нет описания';
    const catalogPrice = card.querySelector('span.course-card__price .display-price__price')?.innerText.trim() || '0.0';
    const ratingElement = card.querySelector('span.course-card__widget[data-type="rating"] > span:nth-child(2)');
    const catalogRating = ratingElement ? ratingElement.innerText.trim().split(' ')[0] : '0.0'; // Берем "4.9" из "4.9 (168)"

    const catalogReviews = ratingElement ? ratingElement.innerText.trim().split(' ')[1] : '0'; // Берем "4.9" из "4.9 (168)"

    const catalogLevel = card.querySelector('div.course-card__level')?.innerText.trim() || 'Неизвестно';
    const courseVal = "0";
    console.log(catalogTitle);

    courses.push({
      name: catalogTitle,
      description: catalogDescription,
      price: catalogPrice,
      rating: catalogRating,
      reviews: catalogReviews,
      difficulty: catalogLevel,
      valuate: courseVal
    });
  });
  return courses;
}

// Проверяем, находимся ли мы на странице курса или каталога
if (window.location.href.includes('/course/')) {
  // Если это страница курса, собираем данные
  setTimeout(() => {
    const courseData = collectCourseData();
    chrome.runtime.sendMessage({ action: 'collectData', data: courseData });
  }, 3000);
} else if (window.location.href.includes('/catalog/')) {
  setTimeout(() => {
    const catalogData = collectCatalogData();
    console.log('Данные каталога после задержки:', catalogData);
    catalogData.forEach(course => {
      chrome.runtime.sendMessage({ action: 'collectData', data: course });
    });
  }, 8000);
}
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'collectCourseData') {
    const courseData = collectCourseData();
    sendResponse({ data: courseData });
  }
});