document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".table-attendance").forEach(
    (table) =>
      new DataTable(table, {
        paging: false,
        searching: false,
        info: false,
        order: [],
        columns: [
          { orderable: false },
          null,
          null,
          null,
          { orderable: false },
          { orderable: false },
        ],
      })
  );
});
