const modalElement = document.getElementById("modal");
const modal = new bootstrap.Modal(modalElement);
const form = document.getElementById("form");
const inputIndex = document.getElementById("id_index");

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
    inputIndex.value = button.dataset.index;

    const window = modalElement.querySelector(
      `[data-index="${button.dataset.index}"`
    );
    const element = window || form;

    element.classList.remove("d-none");
  })
);

modalElement.addEventListener("hide.bs.modal", () => {
  modalElement
    .querySelector(".modal-content:not(.d-none)")
    .classList.add("d-none");
  document.querySelector(".opened").classList.remove("opened");
});
