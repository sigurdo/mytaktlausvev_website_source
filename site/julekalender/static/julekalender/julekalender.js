const modal = $("#newWindow");
modal.on("show.bs.modal", function (event) {
  const windowIndex = $(event.relatedTarget).data("index");
  modal.find("#id_index").val(windowIndex);
});
