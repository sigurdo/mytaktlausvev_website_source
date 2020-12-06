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
const windowForm = document.getElementById("window-form");
const modalTitle = document.querySelector(".modal-title");
const modalEdit = document.querySelector(".modal-edit");

const windowAuthor = windowContent.querySelector(".window-author");
const windowText = windowContent.querySelector(".window-text");
function showWindow() {
  const window = writtenWindows.find((window) => window.index == selectedIndex);
  modalTitle.textContent = window.title;
  windowAuthor.textContent = window.author;
  windowText.textContent = window.content;
  modalEdit.style.display = window.canEdit ? "block" : "none";

  windowContent.style.display = "block";
  windowForm.style.display = "none";
}

function showEditWindow() {
  const window = writtenWindows.find((window) => window.index == selectedIndex);
  setFormValues(window.title, window.content, window.index, "Endre luke");
  modalTitle.textContent = "Endre luke";
  modalEdit.style.display = "none";

  windowContent.style.display = "none";
  windowForm.style.display = "block";
}

function showNewWindow() {
  setFormValues(
    localStorage.getItem(`julekalender-autosave-title-${selectedIndex}`) || "",
    localStorage.getItem(`julekalender-autosave-content-${selectedIndex}`) ||
      "",
    selectedIndex,
    "Legg ut"
  );
  modalTitle.textContent = "Ny luke";
  modalEdit.style.display = "none";

  windowContent.style.display = "none";
  windowForm.style.display = "block";
}

const titleField = document.getElementById("id_title");
const contentField = document.getElementById("id_content");
const indexField = document.getElementById("id_index");
const submitButton = document.getElementById("submit-id-submit");
function setFormValues(title, content, index, buttonText) {
  titleField.value = title;
  contentField.value = content;
  indexField.value = index;
  submitButton.value = buttonText;
}

// Autosave drafts:
titleField.addEventListener("input", () =>
  localStorage.setItem(
    `julekalender-autosave-title-${indexField.value}`,
    titleField.value
  )
);
contentField.addEventListener("input", () =>
  localStorage.setItem(
    `julekalender-autosave-content-${indexField.value}`,
    contentField.value
  )
);