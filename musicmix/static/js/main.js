console.log('script geladen');

function goBack() {
    console.log('Terugknop ingedrukt');
    history.back();
}

// code voor de popover
const popoverLinks = document.querySelectorAll('[data-popover]');
const popovers = document.getElementsByClassName('popover');

document.addEventListener('click', closePopUp)

for (let p in popovers) {
    p.addEventListener('click', openPopUp)
}

// this is the element that fired the event
function openPopUp(event) {
    event.preventDefault();



}

function closePopUp(ignored) {
    for (let p in popovers) {

        if (popoverOpened(this)) {
            p.classList.remove('popover-open');
        }
    }
}

function fetchCurrentElement(element) {
    let href = element.getAttribute('href');
    return document.querySelector(href);
}

function popoverOpened(element) {
    let list = fetchCurrentElement(element);
    return list.classList.contains('popover-open');
}
