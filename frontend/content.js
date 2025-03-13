function collectCourseData() {
  const courseTitle = document.querySelector('h1')?.innerText.trim() || 'Нет названия';
  const courseDescription = document.querySelector('meta[name="description"]')?.content || 'Нет описания';
  const coursePrice = document.querySelector('.price')?.innerText.trim() || '0';
  const ratingStars = document.querySelector('.rating')?.innerText.trim() || '0';
  const reviewsCount = document.querySelector('.reviews')?.innerText.trim() || '0';
  const courseDifficulty = document.querySelector('.level')?.innerText.trim() || 'Неизвестно';

  return {
    name: courseTitle,
    description: courseDescription,
    price: coursePrice,
    rating: ratingStars,
    reviews: reviewsCount,
    difficulty: courseDifficulty,
    valuate: "0"  // Добавляем заглушку, чтобы соответствовать модели
  };
}