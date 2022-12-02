/**
 * @brief Recorta una URL.
 *
 * @param URL La URL a recortar.
 * @param callback Función a llamar como respuesta. La función debe
 * aceptar como argumento un objeto con los siguientes atributos:
 *     - "id": ID de la URL creada.
 *     - "long_url": URL original.
 *     - "short_URL": URL corta.
 */
function makeURL(URL, callback) {
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    };
    if (token) {
        headers["Authorization"] = token;
    }
    body = JSON.stringify([
        {
            "url": URL,
            "is_private": false,
            "allow_list": []
        }
    ]);
    fetch("/api/", {
        "method": "POST",
        "headers": headers,
        "body": body
    })
    .then((response) => response.json())
    .then((data) => callback(data[0]))
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
            longURL.value = data.long_url;
            shortURL.value = data.short_url;
        })
    );

    remakeShortURL.addEventListener("click", () => {
        inputForm.classList.toggle("d-none");
        outputForm.classList.toggle("d-none");
    });
}