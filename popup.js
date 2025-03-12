document.addEventListener("DOMContentLoaded", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const url = tabs[0].url;

    // Отправляем запрос в background.js
    chrome.runtime.sendMessage({ action: "parseCourse", url: url }, (response) => {
      if (response) {
        document.getElementById("courseTitle").textContent = response.title;
        document.getElementById("courseDescription").textContent = response.description;
      } else {
        document.getElementById("courseTitle").textContent = "Ошибка";
        document.getElementById("courseDescription").textContent = "Не удалось получить данные";
      }
    });
  });
});