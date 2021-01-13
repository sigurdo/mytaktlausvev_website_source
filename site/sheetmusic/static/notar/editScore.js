// Getting CSRF token:
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrfToken = getCookie('csrftoken');



// Registering all event listeners:

// Buttons for deleting pdfs from list
let deletePdfButtons = document.querySelectorAll('.delete-pdf');
for (let i = 0; i < deletePdfButtons.length; i++) {
    deletePdfButtons[i].addEventListener('click', ev => {
        let button = ev.target;
        let pk = button.getAttribute('data-pk');
        let displayname = button.getAttribute('data-displayname');
        let p = button.parentNode;
        if (!confirm(`Er du sikker på at du vil slette ${displayname}?`)) return;
        fetch(new Request(`/notar/rest/pdf/${pk}`, {
            headers: { 'X-CSRFToken': csrfToken },
            method: 'DELETE',
            mode: 'same-origin'
        })).then(response => {
            if (response.ok) {
                trsToDelete = document.querySelectorAll(`.part-tr[data-pdf-pk="${pk}"]`);
                for (let j = 0; j < trsToDelete.length; j++) {
                    trsToDelete[j].parentNode.removeChild(trsToDelete[j]);
                }
                p.parentNode.removeChild(p);
            }
        });
    });
}

// Buttons for deleting parts from list
let deletePartButtons = document.querySelectorAll('.delete-part');
for (let i = 0; i < deletePartButtons.length; i++) {
    deletePartButtons[i].addEventListener('click', ev => {
        let button = ev.target;
        let tr = button.parentNode.parentNode;
        if (!confirm(`Er du sikker på at du vil slette ${button.getAttribute('data-name')}?`)) return;
        fetch(new Request(`/notar/rest/part/${button.getAttribute('data-pk')}`, {
            headers: { 'X-CSRFToken': csrfToken },
            method: 'DELETE',
            mode: 'same-origin'
        })).then(response => {
            if (response.ok) tr.parentNode.removeChild(tr);
        });
    });
}



// Fetch pdf processing statuses:
let pdfProcessingStatusSpans = document.querySelectorAll('.pdf-processing-status');
for (let i = 0; i < pdfProcessingStatusSpans.length; i++) {
    let fetchFunction = () => {
        let span = pdfProcessingStatusSpans[i];
        fetch(new Request(`/notar/rest/pdf/processingstatus/${span.getAttribute('data-pk')}`, {
            headers: { 'X-CSRFToken': csrfToken },
            method: 'GET',
            mode: 'same-origin'
        })).then(response => response.json()).then(({ processing }) => {
            if (processing) return setTimeout(fetchFunction, 1000);
            if (confirm(`Prosessering av ${span.getAttribute('data-displayname')} er ferdig, vil du laste siden på nytt?`)) location.reload();
            span.parentNode.removeChild(span);
        });
    }
    setTimeout(fetchFunction, 1000);
}
