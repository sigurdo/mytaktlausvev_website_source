
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

// This is a hack to make the first option in the pdf select be a default value because for some reason a django modelform does not accept initial values for foreign key choices fields
let selects = document.querySelectorAll('select');
for (let i = 0; i < selects.length; i++) {
    select = selects[i];
    if (select.length > 1) {
        select.selectedIndex = 1;
    }
}
