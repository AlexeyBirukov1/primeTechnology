document.addEventListener("DOMContentLoaded", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, { action: "parseCourse" }, (response) => {
      if (response && response.title) {
        document.getElementById("courseTitle").textContent = response.title;
        document.getElementById("coursePrice").textContent = `${response.price} ${response.priceCurrency}`;
        document.getElementById("courseRating").textContent = response.rating;
        document.getElementById("courseRatingCount").textContent = response.ratingCount;
        document.getElementById("courseDifficulty").textContent = response.difficulty;
        document.getElementById("courseLessonsCount").textContent = response.lessonsCount;
        document.getElementById("courseDescription").textContent = response.description;
      } else {
        document.getElementById("courseTitle").textContent = response?.title || "Ошибка";
        document.getElementById("coursePrice").textContent = "Не удалось загрузить";
        document.getElementById("courseRating").textContent = "N/A";
        document.getElementById("courseRatingCount").textContent = "0";
        document.getElementById("courseDifficulty").textContent = "N/A";
        document.getElementById("courseLessonsCount").textContent = "N/A";
        document.getElementById("courseDescription").textContent = response?.description || "Неизвестная ошибка";
      }
    });
  });
});