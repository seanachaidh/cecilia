const chips = function() {
    const init = function() {
        const elems = document.getElementsByClassName('chip');
        elems.forEach(element => {
            const label = element.getElementsByTagName('label')[0];
            // ik verwacht maar 1 element
            console.log('Chip ontdekt: ' + label.innerText);
            //TODO moet hier een bind bij zijn?
            element.addEventListener("click", clickEventHandler);
        });
    }

    const clickEventHandler = function() {
        
    }

    init();
}