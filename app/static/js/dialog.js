String.format = function () {
    var s = arguments[0];
    for (var i = 0; i < arguments.length - 1; i++) {
        var reg = new RegExp("\\{" + i + "\\}", "gm");
        s = s.replace(reg, arguments[i + 1]);
    }
    return s;
}

function open_confirm_dialog(id, dtype) {
    var dialog = document.getElementById(String.format('confirm-dialog-{0}-{1}', id, dtype));
    dialog.addEventListener('close', (e) => {
        console.log("closed");
        document.body.style.overflowY = "";
    });

    dialog.showModal();
    document.body.style.overflowY = "hidden";

}

function close_confirm_dialog(id, dtype) {
    var dialog = document.getElementById(String.format('confirm-dialog-{0}-{1}', id, dtype));

    dialog.close();
    

}

function open_image_dialog(id) {
    var dialog = document.getElementById(String.format('image-dialog-{0}', id));
    dialog.addEventListener('close', (e) => {
        console.log("closed");
        document.body.style.overflowY = "";
    });

    dialog.showModal();
    document.body.style.overflowY = "hidden";

}

function close_image_dialog(id) {
    var dialog = document.getElementById(String.format('image-dialog-{0}', id));

    dialog.close();
    

}