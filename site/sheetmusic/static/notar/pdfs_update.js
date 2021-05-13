
// Buttons for deleting pdfs from list
let deletePdfButtons = document.querySelectorAll('.delete-pdf');
for (let i = 0; i < deletePdfButtons.length; i++) {
    deletePdfButtons[i].addEventListener('click', ev => {
        let button = ev.target;
        let pk = button.getAttribute('data-pk');
        let displayname = button.getAttribute('data-displayname');
        let tr = button.parentNode.parentNode;
        if (!confirm(`Er du sikker på at du vil slette ${displayname}?`)) return;
        fetchWithCsrf('DELETE', `/notar/fetch/pdf/${pk}`).then(response => {
            if (response.ok) {
                // trsToDelete = document.querySelectorAll(`.part-tr[data-pdf-pk="${pk}"]`);
                // for (let j = 0; j < trsToDelete.length; j++) {
                //     trsToDelete[j].parentNode.removeChild(trsToDelete[j]);
                // }
                tr.parentNode.removeChild(tr);
            }
        });
    });
}

