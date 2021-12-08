document.addEventListener('DOMContentLoaded', () => {
    new DataTable('#instrument_overview', {
        "order": [[2, "asc"]],
        "paging": false,
        "language": {
            "zeroRecords": "Ingen instrument funne",
            // Would otherwise say "showing page 1 of 1" even though we've turned off paging
            "info": "",
            "infoEmpty": "Ingen instrument funne",
            "infoFiltered": "(filtrert fra totalt _MAX_ instrument)",
            "search": "Søk:",
        }
    });
} );
