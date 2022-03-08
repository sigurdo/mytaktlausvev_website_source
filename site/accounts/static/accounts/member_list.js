document.addEventListener("DOMContentLoaded", () => {
  let data_table = new DataTable("#member_overview", {
    order: [
      [2, "asc"],
      [1, "asc"],
    ],
    paging: false,
    language: {
      zeroRecords: "Ingen medlemmar funne",
      info: "Visar _TOTAL_ medlemmar",
      infoEmpty: "Ingen  medlemmar funne",
      infoFiltered: "(filtrert fra totalt _MAX_ medlemmar)",
      search: "Søk:",
    },
    columns: [
      { orderable: false },
      null,
      { orderData: [2, 1] },
      null,
      { orderable: false },
      { orderable: false },
    ],
  });

  // Filter on membership status when that select gets an input
  document
    .querySelector("#select-membership-status")
    .addEventListener("input", (event) => {
      data_table
        .column(2)
        .search(
          event.target.value ? "^" + event.target.value + "$" : "",
          true,
          false
        )
        .draw();
    });
});
