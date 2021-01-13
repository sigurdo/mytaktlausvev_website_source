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
        let p = button.parentNode;
        if (!confirm(`Er du sikker på at du vil slette ${button.getAttribute('data-displayname')}?`)) return;
        fetch(new Request(`/notar/rest/pdf/${button.getAttribute('data-pk')}`, {
            headers: { 'X-CSRFToken': csrfToken },
            method: 'DELETE',
            mode: 'same-origin'
        })).then(response => {
            if (response.ok) p.parentNode.removeChild(p);
        });
    });
}

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
