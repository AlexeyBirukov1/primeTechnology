function parseCourseData() {
  // Название
  const title = document.querySelector("h1.course-promo__header")?.textContent.trim() || "Название курса не найдено";

  // Описание
  const description = document.querySelector("div.course-promo__description")?.textContent.trim() || "Описание не найдено";

  // Сложность
  const difficultyElement = document.querySelector('div.course-promo__head-widget[data-type="difficulty"]');
  const difficulty = difficultyElement ? difficultyElement.textContent.trim().replace(/^\s*Средний уровень\s*$/, "Средний") : "Сложность не найдена";

  // Количество уроков
  const lessonsElement = document.querySelector('div.course-promo-includes li b');
  const lessonsCount = lessonsElement ? `${lessonsElement.textContent.trim()} уроков` : "Количество уроков не указано";

  // Цена
  const priceElement = document.querySelector(".format-price");
  let price = 0;
  let priceCurrency = "RUB"; // Форсируем RUB, как ты попросил
  if (priceElement) {
    const priceParts = Array.from(priceElement.querySelectorAll('span[data-type="integer"]'))
      .map(part => part.textContent.trim())
      .join("");
    price = parseFloat(priceParts) || 0;
  }

  // Дополнительные данные из JSON-LD (fallback)
  const jsonLdScript = document.querySelector('script[type="application/ld+json"]');
  let additionalData = {};
  if (jsonLdScript) {
    try {
      const jsonData = JSON.parse(jsonLdScript.textContent);
      additionalData = {
        price: parseFloat(jsonData.offers?.price) || price,
        priceCurrency: jsonData.offers?.priceCurrency || priceCurrency,
        rating: parseFloat(jsonData.aggregateRating?.ratingValue) || 0,
        ratingCount: parseInt(jsonData.aggregateRating?.ratingCount) || 0,
      };
    } catch (e) {
      console.error("Ошибка парсинга JSON-LD:", e);
    }
  }

  const courseData = {
    title,
    description,
    price: price || additionalData.price,
    priceCurrency: priceCurrency || additionalData.priceCurrency,
    rating: additionalData.rating,
    ratingCount: additionalData.ratingCount,
    difficulty,
    lessonsCount
  };

  // Форматируем цену с пробелом
  const formattedPrice = courseData.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");

  const sortedCourseData = {
    title: courseData.title,
    price: formattedPrice, // "1 490" вместо "1490"
    rating: courseData.rating,
    difficulty: courseData.difficulty,
    lessonsCount: courseData.lessonsCount,
    description: courseData.description,
    priceCurrency: courseData.priceCurrency,
    ratingCount: courseData.ratingCount
  };

  return sortedCourseData;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "parseCourse") {
    // Ждём динамическую загрузку данных
    setTimeout(() => {
      const courseData = parseCourseData();
      sendResponse(courseData);
    }, 2000); // Задержка 1 секунда
    return true; // Асинхронный ответ
  }
});