window.addEventListener("load", () => {
  document
    .querySelectorAll("[class^=autocompleteselect]")
    .forEach((element) => {
      if (element.tomselect) return;

      const settings = {
        allowEmptyOption: true,
        plugins: ["dropdown_input"],
      };
      new TomSelect(element, settings);
    });
});
