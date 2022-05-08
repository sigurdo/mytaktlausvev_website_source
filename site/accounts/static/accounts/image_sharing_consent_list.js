document.addEventListener("DOMContentLoaded", () => {
  new DataTable("#image-sharing-consent-table", {
    order: [
      [1, "asc"],
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
  });
});
