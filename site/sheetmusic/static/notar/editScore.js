


// Registering all event listeners:


// Inputs for changing part names:
let partNameInputs = document.querySelectorAll('input.part-name');
for (let i = 0; i < partNameInputs.length; i++) {
    let input = partNameInputs[i];
    let pk = input.getAttribute('data-pk');
    let feedbackSpan = document.querySelector(`#error-feedback-msg-${pk}`);
    let feedbackP = feedbackSpan.parentNode;
    let giveFeedback = msg => {
        feedbackSpan.innerHTML = msg;
        feedbackP.removeAttribute('hidden');
    }
    let clearFeedback = () => {
        feedbackP.setAttribute('hidden', '');
        feedbackSpan.innerHTML = '';
    }
    input.addEventListener('input', ev => {
        fetchWithCsrf('PUT', `/notar/fetch/part/${pk}`, { name: input.value }).then(async response => {
            if (response.ok) clearFeedback();
            else giveFeedback(await response.text());
        })
    })
}

// Inputs for changing part pagenumbers:
let partPagenumbersInputs = document.querySelectorAll('input.part-pagenumbers');
for (let i = 0; i < partPagenumbersInputs.length; i++) {
    let input = partPagenumbersInputs[i];
    let pk = input.getAttribute('data-pk');
    let feedbackSpan = document.querySelector(`#error-feedback-msg-part-pagenumbers-${pk}`);
    let feedbackP = feedbackSpan.parentNode;
    let giveFeedback = msg => {
        feedbackSpan.innerHTML = msg;
        feedbackP.removeAttribute('hidden');
    }
    let clearFeedback = () => {
        feedbackP.setAttribute('hidden', '');
        feedbackSpan.innerHTML = '';
    }
    input.addEventListener('input', ev => {
        const wrongFormatMessage = 'Sidenummer må være på formatet &ltsidenummer&gt eller &ltførste sidenummer&gt-&ltsiste sidenummer&gt. Alle sidenumer må være heltall og siste sidenummer må være større enn det første.';
        let pageNumbers = input.value.split('-');
        let fromPage;
        let toPage;
        if (pageNumbers.length == 1) {
            fromPage = Number(pageNumbers[0])
            toPage = fromPage;
        }
        else if (pageNumbers.length == 2) {
            fromPage = Number(pageNumbers[0]);
            toPage = Number(pageNumbers[1]);
        }
        else return giveFeedback(wrongFormatMessage);
        if (isNaN(fromPage) ||  isNaN(toPage) || fromPage <= 0 || toPage <= 0 || fromPage % 1 != 0 || toPage % 1 != 0 || toPage < fromPage) {
            return giveFeedback(wrongFormatMessage);
        }
        fetchWithCsrf('PUT', `/notar/fetch/part/${pk}`, { fromPage, toPage }).then( async response => {
            if (response.ok) clearFeedback();
            else giveFeedback(await response.text());
        });
    });
}



// Fetch pdf processing statuses:
let pdfProcessingStatusSpans = document.querySelectorAll('.pdf-processing-status');
for (let i = 0; i < pdfProcessingStatusSpans.length; i++) {
    let span = pdfProcessingStatusSpans[i];
    let fetchFunction = () => {
        fetchWithCsrf('GET', `/notar/fetch/pdf/processingstatus/${span.getAttribute('data-pk')}`).then(async response => {
            if (response.ok) {
                let { processing } = await response.json();
                if (processing) return setTimeout(fetchFunction, 1000);
                if (confirm(`Prosessering av ${span.getAttribute('data-displayname')} er ferdig, vil du laste siden på nytt?`)) location.reload();
                span.parentNode.removeChild(span);
            }
        });
    }
    setTimeout(fetchFunction, 1000);
}
