
// Registering all event listeners:
// Buttons for deleting scores from list
let deleteButtons = document.querySelectorAll('.delete-score');
for (let i = 0; i < deleteButtons.length; i++) {
    deleteButtons[i].addEventListener('click', ev => {
        let button = ev.target;
        let tr = button.parentNode.parentNode;
        fetchWithCsrf('DELETE', `/notar/fetch/score/${button.getAttribute('data-pk')}`).then(response => {
            if (response.ok) tr.parentNode.removeChild(tr);
        });
    });
}
