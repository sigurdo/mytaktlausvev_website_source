document.querySelector("#ical-link-collapse-button").addEventListener("click", () => {
    let ical_link_collapse_el = document.querySelector("#ical-link-collapse")
    let ical_link_collapse = new bootstrap.Collapse(ical_link_collapse_el, {
        toggle: false,
    });
    let ical_link_a = document.querySelector("#ical-link");
    let feedback_span = document.querySelector("#ical-link-collapse-clipboard-feedback");
    try {
        navigator.clipboard.writeText(ical_link_a.href).then(() => {
            feedback_span.innerHTML = "vart kopiert til utklippstavla di."
        }, () => {
            throw Error()
        });   
    }
    catch (err) {
        feedback_span.innerHTML = "vart dessverre ikkje kopiert automatisk til utklippstavla di, men det klarar du sikkert på eiga hand."
    }
    ical_link_collapse.show();
});
