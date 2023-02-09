document.addEventListener("DOMContentLoaded", () => {
    new DataTable("#instrument-group-leader-table", {
        order: [[1, "asc"]],
        paging: false,
        language: {
            zeroRecords: "Ingen instrumentgruppeleiarar funne",
            // Would otherwise say "showing page 1 of 1" even though we've turned off paging
            info: "",
            infoEmpty: "Ingen instrumentgruppeleiarar funne",
            infoFiltered: "(filtrert fra totalt _MAX_ instrumentgruppeleiarar)",
            search: "Søk:",
        },
        columns: [
            { orderable: false },
            null,
            null,
        ],
    });
});
