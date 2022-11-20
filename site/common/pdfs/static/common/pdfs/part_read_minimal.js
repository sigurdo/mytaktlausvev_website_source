/*
 * Mostly waterfall-boiled from https://mozilla.github.io/pdf.js/examples/index.html#interactive-examples
 */

let pdf_url = document.querySelector('#pdf_url').dataset.pdfUrl;
let canvas_container = document.querySelector('#canvas-container');

pdfjsLib.getDocument(pdf_url).promise.then(pdf => {
    // Generate HTML in separate for loop since selectors get outdated
    // when a parent's `.innerHTML` is updated.
    for (let i = 1; i <= pdf.numPages; i++) {
        canvas_container.innerHTML += `<canvas id="canvas-${i}"></canvas>`;
    }
    for (let i = 1; i <= pdf.numPages; i++) {
        pdf.getPage(i).then(page => {
            let scale = 1.5;
            let viewport = page.getViewport({ scale: scale, });
            // Support HiDPI-screens.
            let outputScale = window.devicePixelRatio || 1;
        
            let canvas = document.querySelector(`#canvas-${i}`);
            let context = canvas.getContext('2d');
        
            canvas.width = Math.floor(viewport.width * outputScale);
            canvas.height = Math.floor(viewport.height * outputScale);
        
            // Cannot simply set `max-width: 100%`, since it will break zooming to
            // more than 100% on PC.
            if (window.innerWidth < 1000) {
                canvas.style.width = "100%";
            }
        
            let transform = outputScale !== 1 ?
                [outputScale, 0, 0, outputScale, 0, 0] :
                null;
        
            let renderContext = {
                canvasContext: context,
                transform: transform,
                viewport: viewport
            };
            page.render(renderContext);
        });
    }
});
