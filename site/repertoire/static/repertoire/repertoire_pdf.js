const iframe = document.querySelector("iframe");

document.querySelectorAll("select[name*='part']").forEach((input) => {
    const handler = () => setPdfSrc(input.options[input.selectedIndex].dataset.pdfUrl)
    input.addEventListener("input", handler);
    input.addEventListener("focus", handler);
});

function setPdfSrc(url) {
    if (url) iframe.src = url;
}
