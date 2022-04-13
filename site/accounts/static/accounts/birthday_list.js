document.addEventListener("DOMContentLoaded", () => {
  new DataTable("#birthday-table", {
    order: [[1, "asc"]],
    paging: false,
    language: {
      zeroRecords: "Ingen medlemmar funne",
      info: "Visar _TOTAL_ medlemmar",
      infoEmpty: "Ingen  medlemmar funne",
      infoFiltered: "(filtrert fra totalt _MAX_ medlemmar)",
      search: "Søk:",
    },
  });
});
