
// Buttons for deleting parts from list
let deletePartButtons = document.querySelectorAll('.delete-part');
for (let i = 0; i < deletePartButtons.length; i++) {
    deletePartButtons[i].addEventListener('click', ev => {
        ev.preventDefault();
        let button = ev.target;
        let tr = button.parentNode.parentNode;
        if (!confirm(`Er du sikker på at du vil slette ${button.getAttribute('data-name')}?`)) return;
        fetchWithCsrf('DELETE', `/notar/fetch/part/${button.getAttribute('data-pk')}`).then(response => {
            if (response.ok) tr.parentNode.removeChild(tr);
        });
    });
}
