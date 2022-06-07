/*
 * Automatically change displayed PDF page
 * when tabbing into and changing from and to pages.
 *
 * Pre-populate from and to pages with suggested values.
 */

const form = document.querySelector("form");
const iframe = document.querySelector("iframe");
const iframeSrcBase = iframe.src;

form.addEventListener("input", (event) => {
  if (event.target.name?.includes("page")) setPdfPage(event.target.value);
});

form.addEventListener("focusin", (event) => {
  if (event.target.name?.includes("from_page")) {
    if (!event.target.value) {
      const previousToPage = getPreviousToPage(event.target);
      if (previousToPage) event.target.value = previousToPage + 1;
    }

    setPdfPage(event.target.value);
  } else if (event.target.name?.includes("to_page")) {
    if (!event.target.value)
      event.target.value = getPreviousFromPage(event.target);

    setPdfPage(event.target.value);
  }
});

function setPdfPage(page) {
  if (page) iframe.src = `${iframeSrcBase}#page=${page}`;
}

function getPreviousToPage(input) {
  const previousRow = input.closest("tr").previousElementSibling;
  if (!previousRow) return;
  return Number(previousRow.querySelector("input[name*='to_page']").value);
}

function getPreviousFromPage(input) {
  const row = input.closest("tr");
  return row.querySelector("input[name*='from_page']").value;
}
