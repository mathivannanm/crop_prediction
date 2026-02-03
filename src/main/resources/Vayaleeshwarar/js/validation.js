function validateForm() {
    const user = document.getElementById("username").value.trim();
    const pass = document.getElementById("password").value.trim();

    if (user === "" || pass === "") {
        alert("All fields are required.");
        return false; // prevents form submission
    }

    return true; // form is valid
}
