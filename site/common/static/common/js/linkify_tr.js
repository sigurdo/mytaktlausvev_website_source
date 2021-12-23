// Makes closest parent tr of all a.linkify-tr a functional link
document.querySelectorAll("a.linkify-tr").forEach(element => {
    element.closest("tr").addEventListener("click", event => {
        if (event.target.tagName.toLowerCase() != "a") {
            window.location = element.href
        }
    });
});
