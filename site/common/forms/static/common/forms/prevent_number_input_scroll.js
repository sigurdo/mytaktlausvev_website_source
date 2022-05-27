/*
 * Prevent unintentionally changing the value of a number
 * input when scrolling
 */

document.addEventListener("wheel", () => {
    if(document.activeElement.type === "number"){
        let element = document.activeElement;
        element.blur();
        window.setTimeout(() => {
            element.focus();
        }, 1);
    }
});
