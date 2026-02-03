<?php
session_start();
include "../config/db.php"; // adjust path if needed

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username']);
    $email    = trim($_POST['email']);
    $password = trim($_POST['password']);

    if (empty($username) || empty($email) || empty($password)) {
        echo "Please fill in all fields.";
        exit;
    }

    // Check if username or email already exists
    $stmt = mysqli_prepare($conn, "SELECT Id FROM user_details WHERE User_Name = ? OR email = ?");
    mysqli_stmt_bind_param($stmt, "ss", $username, $email);
    mysqli_stmt_execute($stmt);
    mysqli_stmt_store_result($stmt);

    if (mysqli_stmt_num_rows($stmt) > 0) {
        echo "Username or email already exists!";
        exit;
    }
    mysqli_stmt_close($stmt);

    // Hash the password
    $hashedPassword = password_hash($password, PASSWORD_DEFAULT);

    // Insert new user
    $stmt = mysqli_prepare($conn, "INSERT INTO user_details (User_Name, email, Password, Visit_Count, Last_Visited, Created_At) VALUES (?, ?, ?, 0, NOW(), NOW())");
    mysqli_stmt_bind_param($stmt, "sss", $username, $email, $hashedPassword);
    if (mysqli_stmt_execute($stmt)) {
        echo "Registration successful! You can now login.";
        header("Location: login.php");
        exit;
    } else {
        echo "Error: Could not register user.";
    }
    mysqli_stmt_close($stmt);
}

mysqli_close($conn);
?>
