document.addEventListener("DOMContentLoaded", () => {
  const dataTable = new DataTable("#table-balance", {
    order: [[1, "asc"]],
    paging: false,
    language: {
      zeroRecords: "Ingen brukarar funne",
      info: "Visar _TOTAL_ brukarar",
      infoEmpty: "Ingen brukarar funne",
      infoFiltered: "(filtrert fra totalt _MAX_ brukarar)",
      search: "Søk:",
    },
    columns: [{ orderable: false }, null, null, null, null, null],
  });

  const filterMembershipStatus = (membershipStatus) => {
    dataTable
      .column(2)
      .search(membershipStatus ? membershipStatus : "", true, false)
      .draw();
  };

  const selectMembershipStatus = document.querySelector(
    "#select-membership-status"
  );

  filterMembershipStatus(selectMembershipStatus.value);
  selectMembershipStatus.addEventListener("input", (event) =>
    filterMembershipStatus(event.target.value)
  );
});
