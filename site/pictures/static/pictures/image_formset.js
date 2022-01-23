const toggleDeletedClass = (checkbox) => {
  checkbox.closest(".form-image").classList.toggle("to-be-deleted");
};

Array.from(document.querySelectorAll('input[id*="DELETE"]')).forEach(
  (checkbox) => {
    if (checkbox.checked) toggleDeletedClass(checkbox);

    checkbox.addEventListener("input", (ev) => toggleDeletedClass(ev.target));
  }
);
