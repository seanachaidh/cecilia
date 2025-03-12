// code voor de popover
const popoverLinks = document.querySelectorAll('[data-popover]');
const popovers = document.getElementsByClassName('popover');

document.addEventListener('click', closePopUp);

for (let popover of popovers) {
    popover.addEventListener('click', openPopUp);
}


// this is the element that fired the event
function openPopUp(event) {
    event.preventDefault();
    console.log('open pop-up');

}

function closePopUp(ignored) {
    for (let p of popovers) {
        if (popoverOpened(p)) {
            p.classList.remove('popover-open');
        }
    }
}

function fetchCurrentElement(element) {
    let href = element.getAttribute('href');
    if (href) {
        return document.querySelector(href);
    }
    return null;
}

function popoverOpened(element) {
    let el = fetchCurrentElement(element);
    if (el !== null) {
        return el.classList.contains('popover-open');
    } else {
        return false;
    }

}
