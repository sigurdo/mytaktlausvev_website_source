document.addEventListener("DOMContentLoaded", () => {
  new DataTable("#storage-access", {
    order: [
      [2, "desc"],
      [0, "asc"],
    ],
    paging: false,
    language: {
      zeroRecords: "Ingen medlemmar funne",
      info: "Visar _TOTAL_ medlemmar",
      infoEmpty: "Ingen medlemmar funne",
      infoFiltered: "(filtrert fra totalt _MAX_ medlemmar)",
      search: "Søk:",
    },
    columns: [null, { orderable: false }, null],
  });
});
