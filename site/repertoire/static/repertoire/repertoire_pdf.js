const iframe = document.querySelector("iframe");

function setPdfSrc(url) {
    const old_url = new URL(iframe.src).pathname
    if (url && url !== old_url) iframe.src = url;
}

const score_select_selector = "select[name*='score']:not([name*='__prefix__'])";
const part_select_selector = "select[name*='part']:not([name*='__prefix__'])";

document.querySelectorAll(part_select_selector).forEach((input) => {
    const handler = () => setPdfSrc(input.options[input.selectedIndex].dataset.pdfUrl);
    input.addEventListener("input", handler);
    input.addEventListener("focus", handler);
});

document.querySelectorAll("tr").forEach(tr => {
    const input = tr.querySelector(part_select_selector);
    if (!input) return;
    const handler = () => setPdfSrc(input.options[input.selectedIndex].dataset.pdfUrl);;
    tr.addEventListener("click", handler);
});

const first_input = document.querySelector(part_select_selector);
setPdfSrc(first_input.options[first_input.selectedIndex].dataset.pdfUrl);
