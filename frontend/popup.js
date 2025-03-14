// popup.js

// Элементы интерфейса
const catalogMode = document.getElementById('catalogMode');
const courseMode = document.getElementById('courseMode');
const compareButton = document.getElementById('compareButton');
const compareButtonCourse = document.getElementById('compareButtonCourse');
const currentCourseRating = document.getElementById('currentCourseRating');
const currentRatingValue = document.getElementById('currentRatingValue');
const recommendedCourse = document.getElementById('recommendedCourse');
const recommendedTitle = document.getElementById('recommendedTitle');
const recommendedDescription = document.getElementById('recommendedDescription');
const recommendedPrice = document.getElementById('recommendedPrice');
const recommendedRating = document.getElementById('recommendedRating');
const recommendedNeuralRating = document.getElementById('recommendedNeuralRating');

// Массив для хранения выбранных уровней
let selectedLevels = [];

// Обработчик нажатия кнопок уровней
document.querySelectorAll('.level-button').forEach(button => {
  button.addEventListener('click', () => {
    // Переключаем состояние кнопки
    button.classList.toggle('active');

    // Добавляем или удаляем уровень из массива selectedLevels
    const level = button.id;
    if (button.classList.contains('active')) {
      selectedLevels.push(level);
    } else {
      selectedLevels = selectedLevels.filter(item => item !== level);
    }

    console.log('Выбранные уровни:', selectedLevels); // Отладочное сообщение
  });
});

// Определяем, на каком сайте находится пользователь
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const url = tabs[0].url;

  if (url.includes('stepik.org/catalog/')) {
    // Режим для каталога
    catalogMode.style.display = 'block';
    courseMode.style.display = 'none';
  } else if (url.includes('/course/')) {
    // Режим для страницы курса
    catalogMode.style.display = 'none';
    courseMode.style.display = 'block';
  }
});

// Обработчик нажатия на кнопку "Сравнить" в режиме каталога
compareButton.addEventListener('click', () => {
  //const catalogTitle = document.querySelectorAll('a.course-card__title')[1]?.innerText.trim();
  const minPrice = parseInt(document.getElementById('minPrice').value) || 0; // Используем parseInt вместо parseFloat
  const maxPriceInput = document.getElementById('maxPrice').value;
  const maxPrice = maxPriceInput ? parseInt(maxPriceInput) : 999999; // Устанавливаем разумный максимум вместо Infinity
  //alert(catalogTitle);
  if (selectedLevels.length === 0) {
    alert('Пожалуйста, выберите хотя бы один уровень курса.');
    return;
  }

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      function: () => {
        const elements = document.querySelectorAll('a.course-card__title');
        console.log('Elements found:', elements.length, elements);
        return elements[1]?.innerText.trim() || 'Нет названия';
      }
    }, (results) => {
      const catalogTitle = results[0].result;
      console.log('Catalog title from script:', catalogTitle);

      console.log('Sending request:', {
        min_price: minPrice,
        max_price: maxPrice,
        difficulties: selectedLevels,
        name: catalogTitle
      });
      fetch('http://127.0.0.1:8000/get_recommended_course', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          min_price: minPrice,       // Приводим к ожидаемому имени
          max_price: maxPrice,       // Приводим к ожидаемому имени
          difficulties: selectedLevels, // Используем "difficulties" вместо "levels"
          name: catalogTitle
        })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        recommendedCourse.classList.remove('hidden');
        recommendedTitle.textContent = data.recommendedCourse.title;
        recommendedDescription.textContent = data.recommendedCourse.description;
        recommendedPrice.textContent = data.recommendedCourse.price;
        recommendedRating.textContent = data.recommendedCourse.rating;
        recommendedNeuralRating.textContent = data.recommendedCourse.neuralRating;
      })
      .catch(error => {
        console.error('Ошибка при запросе данных:', error);
      });
    });
  }); // Добавлена закрывающая скобка для chrome.tabs.query
}); // Добавлена закрывающая скобка для compareButton.addEventListener

// Обработчик нажатия на кнопку "Сравнить" в режиме страницы курса
compareButtonCourse.addEventListener('click', () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const url = tabs[0].url;

    // Запрашиваем оценку текущего курса у backend
    fetch(`http://127.0.0.1:8000/get_course_evaluation?link=${encodeURIComponent(url)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      // Отображаем оценку текущего курса
      currentCourseRating.classList.remove('hidden');
      currentRatingValue.textContent = data.currentCourseRating;
    })
    .catch(error => {
      console.error('Ошибка при запросе данных:', error);
    });
  });
});