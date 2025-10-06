const closeButtons = document.getElementsByClassName("material-symbols-outlined");

Array.from(closeButtons).forEach(element => {
    element.addEventListener("click", () => {
        element.parentElement.remove();
    });
});