<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login / Register</title>
    <link rel="stylesheet" href="css/style.css">
    <style>
        /* Basic Glassmorphism Style */
        body {
            font-family: Arial, sans-serif;
            background: url('images/bg.jpg') no-repeat center center fixed;
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .container {
            width: 380px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            color: #fff;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }

        h2 {
            text-align: center;
            margin-bottom: 20px;
        }

        input {
            width: 100%;
            padding: 12px 10px;
            margin: 8px 0;
            border: none;
            border-radius: 8px;
        }

        button {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            border: none;
            border-radius: 8px;
            background-color: #4caf50;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }

        .switch-btn {
            text-align: center;
            margin-top: 15px;
        }

        .switch-btn a {
            color: #00bfff;
            cursor: pointer;
            text-decoration: none;
        }

        .options {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.9em;
        }

        .hidden {
            display: none;
        }
    </style>
    <script>
        // Form Validation
        function validateLogin() {
            const user = document.getElementById("login-username").value.trim();
            const pass = document.getElementById("login-password").value.trim();
            if (user === "" || pass === "") {
                alert("All fields are required for login.");
                return false;
            }
            return true;
        }

        function validateRegister() {
            const username = document.getElementById("reg-username").value.trim();
            const email = document.getElementById("reg-email").value.trim();
            const password = document.getElementById("reg-password").value.trim();
            const confirm = document.getElementById("reg-confirm").value.trim();

            if (username === "" || email === "" || password === "" || confirm === "") {
                alert("All fields are required for registration.");
                return false;
            }

            const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
            if (!emailPattern.test(email)) {
                alert("Please enter a valid email.");
                return false;
            }

            if (password !== confirm) {
                alert("Passwords do not match.");
                return false;
            }

            if (password.length < 6) {
                alert("Password must be at least 6 characters.");
                return false;
            }

            return true;
        }

        // Toggle Forms
        function showLogin() {
            document.getElementById("login-form").classList.remove("hidden");
            document.getElementById("register-form").classList.add("hidden");
        }

        function showRegister() {
            document.getElementById("login-form").classList.add("hidden");
            document.getElementById("register-form").classList.remove("hidden");
        }
    </script>
</head>
<body>

<div class="container">

    <!-- Login Form -->
    <div id="login-form">
        <h2>Login</h2>
        <form action="php/login.php" method="POST" onsubmit="return validateLogin()">
            <input type="text" id="login-username" name="username" placeholder="Username" required>
            <input type="password" id="login-password" name="password" placeholder="Password" required>

            <div class="options">
                <label><input type="checkbox" name="remember"> Remember me</label>
                <a href="#">Forgot Password?</a>
            </div>

            <button type="submit">Login</button>
        </form>
        <div class="switch-btn">
            <p>Don't have an account? <a onclick="showRegister()">Register</a></p>
        </div>
    </div>

    <!-- Register Form -->
    <div id="register-form" class="hidden">
        <h2>Register</h2>
        <form action="php/register.php" method="POST" onsubmit="return validateRegister()">
            <input type="text" id="reg-username" name="username" placeholder="Username" required>
            <input type="email" id="reg-email" name="email" placeholder="Email" required>
            <input type="password" id="reg-password" name="password" placeholder="Password" required>
            <input type="password" id="reg-confirm" name="confirm_password" placeholder="Confirm Password" required>


            <button type="submit">Register</button>
        </form>
        <div class="switch-btn">
            <p>Already have an account? <a onclick="showLogin()">Login</a></p>
        </div>
    </div>

</div>

</body>
</html>
