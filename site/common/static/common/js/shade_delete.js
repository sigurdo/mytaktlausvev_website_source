Array.from(document.querySelectorAll('input[type="checkbox"]')).forEach(checkbox => {
    checkbox.addEventListener('input', ev => {
        ev.target.closest('tr').classList.toggle('to_be_deleted');
    });
});
