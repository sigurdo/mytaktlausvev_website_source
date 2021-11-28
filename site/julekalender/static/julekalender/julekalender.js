const modalElement = document.getElementById("modal");
const modal = new bootstrap.Modal(modalElement);
const formContainer = document.getElementById("form-container");
const form = document.querySelector("form");

document
  .querySelectorAll(".window-test")
  .forEach((test) =>
    document
      .querySelector(`.button-window[data-index="${test.dataset.index}"]`)
      .classList.add("written")
  );

document.querySelectorAll(".button-window").forEach((button) =>
  button.addEventListener("click", () => {
    modal.show();
    button.classList.add("opened");
    form.index.value = button.dataset.index;

    const window = modalElement.querySelector(
      `[data-index="${button.dataset.index}"`
    );
    const element = window || formContainer;

    form.title.value =
      localStorage.getItem(`julekalender-autosave-title-${form.index.value}`) ||
      "";
    form.content.value =
      localStorage.getItem(
        `julekalender-autosave-content-${form.index.value}`
      ) || "";

    element.classList.remove("d-none");
  })
);

modalElement.addEventListener("hide.bs.modal", () => {
  modalElement
    .querySelector(".modal-content:not(.d-none)")
    .classList.add("d-none");
  document.querySelector(".opened").classList.remove("opened");
});

function autoSaveDrafts() {
  form.title.addEventListener("input", () =>
    localStorage.setItem(
      `julekalender-autosave-title-${form.index.value}`,
      form.title.value
    )
  );
  form.content.addEventListener("input", () =>
    localStorage.setItem(
      `julekalender-autosave-content-${form.index.value}`,
      form.content.value
    )
  );
}
autoSaveDrafts();
