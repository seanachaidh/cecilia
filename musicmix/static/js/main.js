/**
 * Initialiseert alles voor een dialoog
 * @param {string} dialogParam parameter van die de id van de dialoog moet voorstellen
 * @param {string} openBtn De button die de dialoog opent
 * @param {string} closeBtn De button die de dialoog stluit
 * @returns {void}
 */
function initializeDialog(dialogParam, closeBtn, openBtn) {
    let dialogElem = document.getElementById(dialogParam);
    let closeElem = document.getElementById(closeBtn);
    let openElem = document.getElementById(openBtn);


    openElem.addEventListener("click", openClick);
    closeElem.addEventListener("click", closeClick);

}

function openClick() {
    
}

function closeClick() {
    
}

