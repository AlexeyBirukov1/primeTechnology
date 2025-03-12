document.addEventListener("DOMContentLoaded", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, { action: "parseCourse" }, (response) => {
      if (response && response.title && response.description) {
        document.getElementById("courseTitle").textContent = response.title;
        document.getElementById("courseDescription").textContent = response.description;
      } else {
        document.getElementById("courseTitle").textContent = response?.title || "Ошибка";
        document.getElementById("courseDescription").textContent = response?.description || "Неизвестная ошибка";
      }
    });
  });
});