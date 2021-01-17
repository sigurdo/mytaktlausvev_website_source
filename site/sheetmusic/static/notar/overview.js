
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
// Buttons for deleting scores from list
let deleteButtons = document.querySelectorAll('.delete-score');
for (let i = 0; i < deleteButtons.length; i++) {
    deleteButtons[i].addEventListener('click', ev => {
        let button = ev.target;
        let p = button.parentNode;
        fetch(new Request(`/notar/fetch/score/${button.getAttribute('data-id')}`, {
            headers: { 'X-CSRFToken': csrfToken },
            method: 'DELETE',
            mode: 'same-origin'
        })).then(response => {
            if (response.ok) p.parentNode.removeChild(p);
        });
    });
}

document.querySelector('#test-fetch').addEventListener('click', () => {
    console.log('Klikka');
    fetch(new Request('/notar/fetch/score/25', {
        headers: { 'X-CSRFToken': csrfToken },
        method: 'DELETE',
        mode: 'same-origin',
        body: JSON.stringify({ title: 'Nytt navn hehey' })
    }));
});
