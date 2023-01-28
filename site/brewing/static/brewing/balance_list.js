document.addEventListener("DOMContentLoaded", () => {
  new DataTable("#table-balance", {
    order: [[1, "asc"]],
    paging: false,
    language: {
      zeroRecords: "Ingen brukarar funne",
      info: "Visar _TOTAL_ brukarar",
      infoEmpty: "Ingen brukarar funne",
      infoFiltered: "(filtrert fra totalt _MAX_ brukarar)",
      search: "Søk:",
    },
    columns: [{ orderable: false }, null, null, null, null],
  });
});
