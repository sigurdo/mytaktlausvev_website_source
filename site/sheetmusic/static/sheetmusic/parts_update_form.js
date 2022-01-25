/*
 * Automatically change displayed PDF page
 * when tabbing into and changing from and to pages.
 *
 * Pre-populate from and to pages with suggested values.
 * 
 * Prevent unintentionally changing the value of a number
 * input when scrolling
 */

const iframe = document.querySelector("iframe");
const iframeSrcBase = iframe.src;

document
  .querySelectorAll("input[name*='page']")
  .forEach((input) =>
    input.addEventListener("input", () => setPdfPage(input.value))
  );

document.querySelectorAll("input[name*='from_page']").forEach((input) => {
  input.addEventListener("focus", () => {
    if (!input.value) {
      const previousToPage = getPreviousToPage(input);
      if (previousToPage) input.value = previousToPage + 1;
    }

    setPdfPage(input.value);
  });
});

document.querySelectorAll("input[name*='to_page']").forEach((input) => {
  input.addEventListener("focus", () => {
    if (!input.value) input.value = getPreviousFromPage(input);

    setPdfPage(input.value);
  });
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

document.addEventListener("wheel", () => {
  if(document.activeElement.type === "number"){
    let element = document.activeElement;
    element.blur();
    window.setTimeout(() => {
      element.focus();
    }, 1);
  }
});
