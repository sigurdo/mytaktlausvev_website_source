const modals = $(".modal");

modals.on("show.bs.modal", (event) => {
  const window = $(event.currentTarget).parent();
  window.addClass("opened");
});
modals.on("hide.bs.modal", (event) => {
  const window = $(event.currentTarget).parent();
  window.removeClass("opened");
});
