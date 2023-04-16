function open_navigation() {
    document.getElementById("before").style.opacity = 0
    document.getElementById("after").style.opacity = 0
    document.getElementById("before").style.visibility = "hidden";
    document.getElementById("after").style.visibility = "hidden";

    document.getElementsByClassName("navigation")[0].style.visibility = "visible";
    document.body.style.overflowY = "hidden";

}

function close_navigation() {
        document.getElementById("before").style.opacity = 1
    document.getElementById("after").style.opacity = 1
    document.getElementById("before").style.visibility = "visible";
    document.getElementById("after").style.visibility = "visible";

    document.getElementsByClassName("navigation")[0].style.visibility = "hidden";
    document.body.style.overflowY = "auto";

}