// popup.js

// Элементы интерфейса
const stepikMode = document.getElementById('stepikMode');
const otherSiteMode = document.getElementById('otherSiteMode');
const compareButton = document.getElementById('compareButton');
const compareButtonOtherSite = document.getElementById('compareButtonOtherSite');
const courseRating = document.getElementById('courseRating');
const courseRatingValue = document.getElementById('courseRatingValue');
const recommendedCourse = document.getElementById('recommendedCourse');
const recommendedTitle = document.getElementById('recommendedTitle');
const recommendedDescription = document.getElementById('recommendedDescription');
const recommendedPrice = document.getElementById('recommendedPrice');
const recommendedRating = document.getElementById('recommendedRating');
const recommendedNeuralRating = document.getElementById('recommendedNeuralRating');

// Определяем, на каком сайте находится пользователь
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const url = tabs[0].url;

  if (url.includes('stepik.org')) {
    // Режим для Stepik
    stepikMode.classList.remove('hidden');
  } else {
    // Режим для других сайтов
    otherSiteMode.classList.remove('hidden');
  }
});

// Обработчик нажатия кнопки "Сравнить" для Stepik
compareButton.addEventListener('click', () => {
  // Запрашиваем оценку нейросети у backend
  chrome.runtime.sendMessage({ action: 'getNeuralNetworkRating' }, (response) => {
    if (response && response.rating) {
      // Отображаем поле "Оценка нейросети"
      neuralRating.classList.remove('hidden');
      ratingValue.textContent = response.rating;
    } else {
      neuralRating.classList.remove('hidden');
      ratingValue.textContent = 'Ошибка';
    }
  });
});

// Обработчик нажатия кнопки "Сравнить" для других сайтов
compareButtonOtherSite.addEventListener('click', () => {
  // Собираем данные о курсе
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, { action: 'collectCourseData' }, (response) => {
      if (response && response.data) {
        // Отправляем данные на backend
        chrome.runtime.sendMessage(
          { action: 'evaluateCourse', data: response.data },
          (backendResponse) => {
            if (backendResponse) {
              // Отображаем оценку курса
              courseRating.classList.remove('hidden');
              courseRatingValue.textContent = backendResponse.courseRating;

              // Отображаем карточку рекомендуемого курса
              recommendedCourse.classList.remove('hidden');
              recommendedTitle.textContent = backendResponse.recommendedCourse.title;
              recommendedDescription.textContent = backendResponse.recommendedCourse.description;
              recommendedPrice.textContent = backendResponse.recommendedCourse.price;
              recommendedRating.textContent = backendResponse.recommendedCourse.rating;
              recommendedNeuralRating.textContent = backendResponse.recommendedCourse.neuralRating;
            } else {
              courseRating.classList.remove('hidden');
              courseRatingValue.textContent = 'Ошибка';
            }
          }
        );
      } else {
        courseRating.classList.remove('hidden');
        courseRatingValue.textContent = 'Не удалось собрать данные';
      }
    });
  });
});