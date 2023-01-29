document.addEventListener("DOMContentLoaded", () => {
  new DataTable("#table-brews", {
    order: [
      [2, "asc"],
      [0, "asc"],
    ],
    paging: false,
    language: {
      zeroRecords: "Ingen brygg funne",
      info: "Visar _TOTAL_ brygg",
      infoEmpty: "Ingen brygg funne",
      infoFiltered: "(filtrert fra totalt _MAX_ brygg)",
      search: "Søk:",
    },
    columns: [null, null, null, { orderable: false }],
  });
});
