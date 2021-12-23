// Makes all elements with class make-link a functional link
document.querySelectorAll(".make-link").forEach(element => {
    element.addEventListener("click", event => {
        if (event.target.tagName.toLowerCase() != "a") {
            window.location = element.attributes.href.nodeValue
        }
    });
});
