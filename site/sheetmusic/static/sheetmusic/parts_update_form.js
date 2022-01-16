const iframe = document.querySelector("iframe");
const iframeSrcBase = iframe.src;

const eventTypes = ["focus", "input"];

document.querySelectorAll("input[name*='page']").forEach((input) => {
  eventTypes.forEach((eventType) =>
    input.addEventListener(eventType, (event) => {
      if (event.target.value)
        iframe.src = `${iframeSrcBase}#page=${event.target.value}`;
    })
  );
});
