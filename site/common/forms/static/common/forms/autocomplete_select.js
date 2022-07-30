window.addEventListener("load", () => {
  document.querySelectorAll(".autocompleteselect").forEach((el) => {
    let settings = {
      allowEmptyOption: true,
      plugins: ["dropdown_input"],
    };
    new TomSelect(el, settings);
  });
});
