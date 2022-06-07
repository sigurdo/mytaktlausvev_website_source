const totalForms = document.querySelector("[name$=TOTAL_FORMS]");
const emptyForm = document.querySelector(".empty-form");
const formsContainer = emptyForm.parentElement;

function resetTotalForms() {
  totalForms.value = formsContainer.childElementCount - 1;
}

function addForm() {
  const newForm = emptyForm.cloneNode(true);
  newForm.classList.remove("d-none", "empty-form");
  renumberForm(newForm, totalForms.value);
  formsContainer.insertAdjacentElement("beforeend", newForm);
  totalForms.value = Number(totalForms.value) + 1;

  newForm
    .querySelector('input[id*="DELETE"]')
    .addEventListener("input", (ev) => toggleDeletedClass(ev.target));
}

function renumberForm(form, newIndex) {
  ["name", "id", "for"].forEach((attr) => {
    form.querySelectorAll(`[${attr}*=__prefix__]`).forEach((element) => {
      const value = element.getAttribute(attr);
      const replaced = value.replace("__prefix__", newIndex);
      element.setAttribute(attr, replaced);
    });
  });
}

window.addEventListener("load", () => {
  resetTotalForms();
  
  const formsetAddButton = document.querySelector("[data-formset-add-form]");
  if (formsetAddButton) {
    formsetAddButton.addEventListener("click", addForm);
  }
});
