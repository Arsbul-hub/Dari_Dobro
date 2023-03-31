String.format = function () {
    var s = arguments[0];
    for (var i = 0; i < arguments.length - 1; i++) {
        var reg = new RegExp("\\{" + i + "\\}", "gm");
        s = s.replace(reg, arguments[i + 1]);
    }
    return s;
}

function open_confirm_remove(id) {
    document.getElementById(String.format('confirm-remove-dialog-{0}', id)).style.visibility = "visible"

    document.body.style.overflow = "hidden"
    document.getElementsByClassName("item-block").style.pointerEvents = "none"
    document.getElementById("all").style.opacity = "0.5"


}

function close_confirm_remove(id) {
    document.getElementById(String.format('confirm-remove-dialog-{0}', id)).style.visibility = "hidden"

    document.body.style.overflow = "visible"
    document.getElementById("all").style.opacity = 1
}

function open_confirm_move(id) {
    document.getElementById(String.format('confirm-move-dialog-{0}', id)).style.visibility = "visible"

    document.body.style.overflow = "hidden"
    document.getElementsByClassName("item-block").style.pointerEvents = "none"

    document.getElementById("all").style.opacity = 0.5
}

function close_confirm_move(id) {
    document.getElementById(String.format('confirm-move-dialog-{0}', id)).style.visibility = "hidden"

    document.body.style.overflow = "visible"
    document.getElementById("all").style.opacity = 1
}