setInterval(async () => {
    const data = JSON.parse((await fetch('{API_ROUTE_PREFIX}/recap')).text())
    for (key in data) document.querySelectorAll(`[data-key="${key}"]`).forEach(element => element.innerHTML = data[key])
}, 10000);