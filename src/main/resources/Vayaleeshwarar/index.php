<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
    <link rel="stylesheet" href="/Vayaleeshwarar/css/style.css">

    <script>
        function validateForm() {
            const user = document.getElementById("username").value.trim();
            const pass = document.getElementById("password").value.trim();

            if (user === "" || pass === "") {
                alert("All fields are required.");
                return false;
            }
            return true;
        }
    </script>
</head>
<body>

<div class="glass-box">
    <h2>Login</h2>

    <form action="/Vayaleeshwarar/php/login.php" method="POST" onsubmit="return validateForm()">
        <input type="text" id="username" name="username" placeholder="Username" required>
        <input type="password" id="password" name="password" placeholder="Password" required>

        <div class="options">
            <label>
                <input type="checkbox" name="remember"> Remember me
            </label>
            <a href="#">Forgot Password?</a>
        </div>

        <button type="submit">Login</button>

        <p style="text-align:center; margin-top:15px;">
            Don't have an account?
            <a href="/Vayaleeshwarar/register.php">Register</a>
        </p>
    </form>
</div>

</body>
</html>
