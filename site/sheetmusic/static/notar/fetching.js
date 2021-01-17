// Getting CSRF token:
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrfToken = getCookie('csrftoken');

/**
 * @param {String} method - The HTTP method to use. Typically either GET, POST, PUT or DELETE
 * @param {String} url - The URL to use.
 * @param {Object=} data - An optional data object to send with the request.
 * @returns {Promise<Response>} Returns a Promise that will resolve with a Response object with data from the server
 */
async function fetchWithCsrf(method, url, data /* optional */) {
    const body = data ? JSON.stringify(data) : undefined;
    return fetch(new Request(url, { method, body,
        headers: { 'X-CSRFToken': csrfToken },
        mode: 'same-origin'
    }));
}
