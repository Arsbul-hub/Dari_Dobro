function show_password() {
    if (document.getElementById("password").type == "password") {
        document.getElementById("password").type = "text"
        document.getElementById("eye").className = "far fa-eye-slash"
    }
    else if (document.getElementById("password").type == "text") {
        document.getElementById("password").type = "password"
        document.getElementById("eye").className = "fas fa-eye"
    }

}