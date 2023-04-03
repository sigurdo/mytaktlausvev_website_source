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
      infoEmpty: "Ingen medlemmar funne",
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
      { orderable: false },
    ],
  });

  const filterMembershipStatus = (membershipStatus) => {
    data_table
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
