document.addEventListener("DOMContentLoaded", () => {
  new DataTable("#score-list", {
    order: [[0, "asc"]],
    paging: false,
    language: {
      zeroRecords: "Inga notar funne",
      info: "Visar _TOTAL_ notar",
      infoEmpty: "Inga notar funne",
      infoFiltered: "(filtrert fra totalt _MAX_ notar)",
      search: "Søk:",
    },
    columns: [null, { orderable: false }, null, null, null],
  });
});
