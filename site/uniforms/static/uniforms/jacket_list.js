document.addEventListener('DOMContentLoaded', () => {
    new DataTable('#jacket_overview', {
        "order": [[0, "asc"]],
        "paging": false,
        "language": {
            "zeroRecords": "Ingen jakker funne",
            // Would otherwise say "showing page 1 of 1" even though we've turned off paging
            "info": "",
            "infoEmpty": "Ingen jakker funne",
            "infoFiltered": "(filtrert fra totalt _MAX_ jakker)",
            "search": "Søk:",
        }
    });
} );
