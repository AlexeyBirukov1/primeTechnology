function parseCourseData() {
  const titleElement = document.querySelector("h1.course-promo__header");
  const title = titleElement ? titleElement.textContent.trim() : "Название курса не найдено";

  const descriptionElement = document.querySelector("div.course-promo__description");
  const description = descriptionElement ? descriptionElement.textContent.trim() : "Описание не найдено";

  return {
    title: title,
    description: description
  };
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "parseCourse") {
    const courseData = parseCourseData();
    sendResponse(courseData);
  }
});