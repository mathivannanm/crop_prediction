<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Register</title>
    <link rel="stylesheet" href="/Vayaleeshwarar/css/style.css">

    <script>
        function validateRegisterForm() {
            const username = document.getElementById("username").value.trim();
            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();
            const confirmPassword = document.getElementById("confirm_password").value.trim();

            if (username === "" || email === "" || password === "" || confirmPassword === "") {
                alert("All fields are required.");
                return false;
            }

            // Simple email format validation
            const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
            if (!emailPattern.test(email)) {
                alert("Please enter a valid email address.");
                return false;
            }

            // Password match validation
            if (password !== confirmPassword) {
                alert("Passwords do not match.");
                return false;
            }

            // Optional: password length check
            if (password.length < 6) {
                alert("Password must be at least 6 characters long.");
                return false;
            }

            return true; // form is valid
        }
    </script>
</head>
<body>

<div class="glass-box">
    <h2>Register</h2>

    <form action="php/register.php" method="POST" onsubmit="return validateRegisterForm()">
        <input type="text" id="username" name="username" placeholder="Username" required>
        <input type="email" id="email" name="email" placeholder="Email" required>
        <input type="password" id="password" name="password" placeholder="Password" required>
        <!-- Added name attribute -->
        <input type="password" id="confirm_password" name="confirm_password" placeholder="Confirm Password" required>

        <button type="submit">Register</button>
        <p>Already have an account? <a href="index.php">Login</a></p>
    </form>
</div>

</body>
</html>
