document.addEventListener("DOMContentLoaded", () => {
  const dataTable = new DataTable("#table-brews", {
    order: [[1, "desc"]],
    paging: false,
    language: {
      zeroRecords: "Ingen brygg funne",
      info: "Visar _TOTAL_ brygg",
      infoEmpty: "Ingen brygg funne",
      infoFiltered: "(filtrert fra totalt _MAX_ brygg)",
      search: "Søk:",
    },
    columns: [
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      { orderable: false },
    ],
  });

  const filterEmptyBrews = (showEmptyBrews) => {
    dataTable
      .column(4)
      .search(showEmptyBrews ? "" : "false", true, false)
      .draw();
  };

  const showEmptyBrews = document.querySelector("#show-empty-brews");

  filterEmptyBrews(showEmptyBrews.checked);
  showEmptyBrews.addEventListener("input", (event) =>
    filterEmptyBrews(event.target.checked)
  );
});
