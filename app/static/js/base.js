function open_top_menu() {
    document.getElementById("navigation").style.display = "block";
    document.getElementById("navigation").style.animation = "base_animation 0.5s forwards";
    document.getElementById("open-navigation").style.display = "none";
    document.getElementById("close-navigation").style.display = "block";


    document.getElementById("before").style.display = "none";
    document.getElementById("after").style.display = "none";


}

function close_top_menu() {
    document.getElementById("navigation").style.display = "none";

    document.getElementById("open-navigation").style.display = "block";
    document.getElementById("close-navigation").style.display = "none";
    document.getElementById("before").style.display = "block";
    document.getElementById("after").style.display = "block";

    // document.getElementsByClassName("navigation")[0].style.visibility = "hidden";
    // document.body.style.overflowY = "auto";

}