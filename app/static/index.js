/**
 * @brief Recorta una URL.
 *
 * @param URL La URL a recortar.
 * @param callback Función a llamar como respuesta. La función debe
 * aceptar como argumento un objeto con los siguientes atributos:
 *     - "longURL": La URL original.
 *     - "shortURL": La URL corta.
 *     - "token": Un token para acceder a la URL (cuando es privada).
 */
function makeURL(URL, callback) {
    fetch("/make-url/", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "URLs": [
                {
                    "URL": URL,
                    "isPrivate": false
                }
            ]
        })
    })
    .then((response) => response.json())
    .then((data) => callback(data.URLs[0]))
    .catch((error) => console.error("Error:", error));
}

window.onload = function() {
    const inputForm = document.querySelector("#input-form");
    const URL = document.querySelector("#url");
    const makeShortURL = document.querySelector("#make-short-url");

    const outputForm = document.querySelector("#output-form");
    const longURL = document.querySelector("#long-url");
    const shortURL = document.querySelector("#short-url");
    const remakeShortURL = document.querySelector("#remake-short-url");

    makeShortURL.addEventListener("click",
        () => makeURL(URL.value, (data) => {
            inputForm.classList.toggle("d-none");
            outputForm.classList.toggle("d-none");
            longURL.value = data.longURL;
            shortURL.value = data.shortURL;
        })
    );

    remakeShortURL.addEventListener("click", () => {
        inputForm.classList.toggle("d-none");
        outputForm.classList.toggle("d-none");
    });
}