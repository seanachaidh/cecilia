// code voor de popover
const popoverLinks = document.querySelectorAll('[data-popover]');

document.addEventListener('click', closePopUp);

for (let popover of popoverLinks) {
    popover.addEventListener('click', openPopUp);
}

function openPopUp(event) {
    event.stopPropagation();
    const href = event.target.getAttribute('href');
    const popover = document.querySelector(href);
    popover.classList.add('popover-open');

}

function closePopUp(ignored) {
    console.log('close popup');
    const popoverElement = fetchCurrentElement()
    if (popoverElement !== null) {
        console.log('Found element. Removing...');
        popoverElement.classList.remove('popover-open');
        window.location.hash = "";
    }

}

function fetchCurrentElement() {
    const hash = window.location.hash;
    console.log('Found hash',  hash);
    if (hash) {
        return document.querySelector(hash);
    }
    return null;
}
