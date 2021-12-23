// Makes all #{data-larger-link-target}-tr clickable links for a corresponding link with the larger-link class
document.querySelectorAll(".larger-link").forEach(link => {
    document.querySelectorAll(link.dataset.largerLinkTarget).forEach(target => {
        target.style.cursor = "pointer";
        target.addEventListener("click", event => {
            if (event.target.tagName.toLowerCase() != "a") {
                link.click();
            }
        });
    });
});
