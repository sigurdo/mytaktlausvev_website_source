const toggleDeletedClass = (checkbox) => {
  checkbox.closest("tr").classList.toggle("to_be_deleted");
};

Array.from(document.querySelectorAll('input[id*="DELETE"]')).forEach(
  (checkbox) => {
    if (checkbox.checked) toggleDeletedClass(checkbox);

    checkbox.addEventListener("input", (ev) => toggleDeletedClass(ev.target));
  }
);
