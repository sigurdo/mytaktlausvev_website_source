const windowTitle = document.getElementById("window-title");
const windowBody = document.getElementById("window-body");
const newWindowTitle = document.getElementById("new-window-title");
const newWindowBody = document.getElementById("new-window-body");

function showWindow(window) {
  windowTitle.textContent = window.title;
  windowBody.textContent = window.content;

  windowTitle.style.display = "block";
  windowBody.style.display = "block";
  newWindowTitle.style.display = "none";
  newWindowBody.style.display = "none";
}

const indexField = document.getElementById("id_index");
function showNewWindow(index) {
  indexField.value = index;

  newWindowTitle.style.display = "block";
  newWindowBody.style.display = "block";
  windowTitle.style.display = "none";
  windowBody.style.display = "none";
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
