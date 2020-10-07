const windowContent = document.getElementById("window-content");
const newWindowContent = document.getElementById("new-window-content");

const windowTitle = windowContent.querySelector(".modal-title");
const windowAuthor = windowContent.querySelector(".modal-author");
const windowText = windowContent.querySelector(".modal-text");
function showWindow(window) {
  windowTitle.textContent = window.title;
  windowAuthor.textContent = window.author;
  windowText.textContent = window.content;

  windowContent.style.display = "block";
  newWindowContent.style.display = "none";
}

const indexField = document.getElementById("id_index");
function showNewWindow(index) {
  indexField.value = index;

  windowContent.style.display = "none";
  newWindowContent.style.display = "block";
}

const windows = JSON.parse(document.getElementById("windows").textContent);
windows.forEach((window) =>
  document.getElementById(`window${window.index}`).classList.add("written")
);

const modal = $(".modal");
function openModal(index) {
  const selectedWindow = windows.find((window) => window.index == index);
  if (selectedWindow) showWindow(selectedWindow);
  else showNewWindow(index);

  document.getElementById(`window${index}`).classList.add("opened");
  modal.modal("toggle");
}

modal.on("hide.bs.modal", () =>
  document.querySelector(".opened").classList.remove("opened")
);
