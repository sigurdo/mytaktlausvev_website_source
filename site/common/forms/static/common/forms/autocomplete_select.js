window.addEventListener("load", () => {
  document.querySelectorAll(".autocompleteselect").forEach((element) => {
    if (element.tomselect) return;

    const settings = {
      allowEmptyOption: true,
      plugins: ["dropdown_input"],
    };
    new TomSelect(element, settings);
  });

  document
    .querySelectorAll(".autocompleteselectmultiple")
    .forEach((element) => {
      if (element.tomselect) return;

      const settings = {
        allowEmptyOption: true,
        plugins: ["dropdown_input", "checkbox_options"],
      };
      new TomSelect(element, settings);
    });
});
