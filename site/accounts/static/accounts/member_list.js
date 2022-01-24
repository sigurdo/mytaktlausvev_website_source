document.addEventListener('DOMContentLoaded', () => {
    new DataTable('#member_overview', {
        "order": [[2, "asc"]],
        "paging": false,
        "language": {
            "zeroRecords": "Ingen medlemar funne",
            // Would otherwise say "showing page 1 of 1" even though we've turned off paging
            "info": "",
            "infoEmpty": "Ingen  medlemar funne",
            "infoFiltered": "(filtrert fra totalt _MAX_ member)",
            "search": "Søk:",
        }
    });
} );
