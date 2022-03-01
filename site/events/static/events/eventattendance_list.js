document.addEventListener('DOMContentLoaded', () => {
    let table = document.querySelector("#attendance_list");
    new DataTable(table, {
        "paging": false,
        "language": {
            "zeroRecords": "Inga svar funne",
            // Would otherwise say "showing page 1 of 1" even though we've turned off paging
            "info": "Visar _TOTAL_ svar",
            "infoEmpty": "Inga svar funne",
            "infoFiltered": "(filtrert fra totalt _MAX_ svar)",
            "search": "Søk:",
        },
        // Code for status filtering, boiled from https://www.datatables.net/examples/api/multi_filter_select.html
        "initComplete": function () {
            this.api().columns().every( function () {
                // Add filters only for column 1 (status) and 2 (instrument group)
                if (this.index() !== 1 && this.index() !== 2) return;
                var column = this;
                var select = $('<select><option value=""></option></select>')
                    .appendTo( $(column.footer()).empty() )
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );
                column.data().unique().sort().each( function ( d, j ) {
                    // Avoid 2 blank options on instrument group filter if there is a user without instrument group
                    if (d === "") return;
                    select.append( '<option value="'+d+'">'+d+'</option>' )
                } );
            } );
        }
    });
} );
