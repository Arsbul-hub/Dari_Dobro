function open_navigation() {
    document.getElementById("close-navigation").style.display = "flex";
    document.getElementById("open-navigation").style.display = "none";

    document.getElementById("navigation").style.opacity = 1;
    document.getElementById("navigation").style.visibility = "visible";
    document.getElementById("navigation").style.height ="100%"
    // document.getElementById("before").style.opacity = 0

    document.getElementById("before").style.display = "none";
    document.getElementById("after").style.display = "none";
    // document.getElementsByClassName("navigation")[0].style.visibility = "visible";
    // document.body.style.overflowY = "hidden";
    // const newspaperSpinning = [
    //       {transform: "translateY(0px)"},
    

    // ];

    // const newspaperTiming = {
    //   duration: 2000,
    //   iterations: 1,
    // };

    // const newspaper = document.getElementById("navigation");

    // newspaper.animate(newspaperSpinning, newspaperTiming);

}

function close_navigation() {
    document.getElementById("close-navigation").style.display = "none";
    document.getElementById("open-navigation").style.display = "flex";
    document.getElementById("navigation").style.height ="0"
    document.getElementById("navigation").style.opacity = 0;
    document.getElementById("navigation").style.visibility = "hidden";
    
    // document.getElementById("before").style.opacity = 1
    // document.getElementById("after").style.opacity = 1
    document.getElementById("before").style.display = "block";
    document.getElementById("after").style.display = "block";

    // document.getElementsByClassName("navigation")[0].style.visibility = "hidden";
    // document.body.style.overflowY = "auto";

}