document.addEventListener('DOMContentLoaded', () => {
    let data_table = new DataTable('#member_overview', {
        "order": [[2, "asc"]],
        "paging": false,
        "language": {
            "zeroRecords": "Ingen medlemar funne",
            // Would otherwise say "showing page 1 of 1" even though we've turned off paging
            "info": "Visar _TOTAL_ medlemmar",
            "infoEmpty": "Ingen  medlemar funne",
            "infoFiltered": "(filtrert fra totalt _MAX_ member)",
            "search": "Søk:",
        }
    });

    // Filter on membership status when that select gets an input
    document.querySelector("#select-membership-status").addEventListener("input", event => {
        let value = $.fn.dataTable.util.escapeRegex(event.target.value);
        data_table.column(2).search( value ? '^'+value+'$' : '', true, false ).draw();
    });
} );
