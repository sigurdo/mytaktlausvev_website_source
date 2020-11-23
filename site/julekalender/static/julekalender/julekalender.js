const writtenWindows = JSON.parse(
  document.getElementById("windows").textContent
);
writtenWindows.forEach((window) =>
  document.getElementById(`window${window.index}`).classList.add("written")
);

let selectedIndex = 1;

function selectWindow(index) {
  selectedIndex = index;
  if (writtenWindows.some((window) => window.index == selectedIndex))
    showWindow();
  else showNewWindow();
  openModal();
}

const modal = $(".modal");
function openModal() {
  document.getElementById(`window${selectedIndex}`).classList.add("opened");
  modal.modal("toggle");
}
modal.on("hide.bs.modal", () =>
  document.querySelector(".opened").classList.remove("opened")
);

const windowContent = document.getElementById("window-content");
const newWindowContent = document.getElementById("new-window-content");

const windowTitle = windowContent.querySelector(".modal-title");
const windowAuthor = windowContent.querySelector(".modal-author");
const windowText = windowContent.querySelector(".modal-text");
const windowChange = windowContent.querySelector(".modal-change");
function showWindow() {
  const window = writtenWindows.find((window) => window.index == selectedIndex);
  windowTitle.textContent = window.title;
  windowAuthor.textContent = window.author;
  windowText.textContent = window.content;

  windowChange.style.display = window.canEdit ? "block" : "none";

  windowContent.style.display = "block";
  newWindowContent.style.display = "none";
}

function showEditWindow() {
  const window = writtenWindows.find((window) => window.index == selectedIndex);
  setFormValues(window.title, window.content, window.index);

  windowContent.style.display = "none";
  newWindowContent.style.display = "block";
}

function showNewWindow() {
  setFormValues("", "", selectedIndex);

  windowContent.style.display = "none";
  newWindowContent.style.display = "block";
}

const titleField = document.getElementById("id_title");
const contentField = document.getElementById("id_content");
const indexField = document.getElementById("id_index");
function setFormValues(title, content, index) {
  titleField.value = title;
  contentField.value = content;
  indexField.value = index;
}
