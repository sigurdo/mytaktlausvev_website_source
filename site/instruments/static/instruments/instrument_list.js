document.addEventListener('DOMContentLoaded', () => {
    new DataTable('#instrument_overview', {
        "order": [[2, "asc"]],
        "language": {
            "lengthMenu": "Vis _MENU_  instrument per side",
            "zeroRecords": "Ingen instrument funne",
            "info": "Viser side _PAGE_ av _PAGES_",
            "infoEmpty": "Ingen instrument funne",
            "infoFiltered": "(filtrert fra totalt _MAX_ instrument)",
            "search": "Søk:",
            "paginate": {
                "first": "Første",
                "last": "Siste",
                "next": "Neste",
                "previous": "Forrige",
            },
        }
    });
} );
