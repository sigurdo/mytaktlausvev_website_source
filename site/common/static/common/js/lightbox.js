const imageElements = document.querySelectorAll("[data-toggle='lightbox']");
imageElements.forEach((image) =>
  image.addEventListener("click", () => {
    BigPicture({
      el: image,
      gallery:
        image.dataset.gallery &&
        document.querySelectorAll(`[data-gallery="${image.dataset.gallery}"`),
      galleryAttribute: "src",
      loop: true,
    });
  })
);
