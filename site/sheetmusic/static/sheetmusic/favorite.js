const forms = document.querySelectorAll(".form-favorite-part");
forms.forEach((form) =>
  form.addEventListener("submit", (event) => {
    event.preventDefault();

    fetchWithCsrf(form.dataset.method, form.action, {
      part_pk: form.part_pk.value,
    }).then(async (response) => {
      if (response.ok) location.reload();
      else console.error("Klarte ikkje å redigere favorittstemme.");
    });
  })
);
