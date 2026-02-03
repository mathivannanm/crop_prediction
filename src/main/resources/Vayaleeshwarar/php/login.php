<?php
session_start();
include "../config/db.php"; // adjust path

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);

    if (empty($username) || empty($password)) {
        echo "Please fill in all fields.";
        exit;
    }

    // Fetch user by username
    $stmt = mysqli_prepare($conn, "SELECT Id, User_Name, Password, Visit_Count FROM user_details WHERE User_Name = ?");
    mysqli_stmt_bind_param($stmt, "s", $username);
    mysqli_stmt_execute($stmt);
    mysqli_stmt_bind_result($stmt, $id, $usernameFetched, $hashedPassword, $visitCount);
    mysqli_stmt_fetch($stmt);
    mysqli_stmt_close($stmt);

    if ($id) {
        if (password_verify($password, $hashedPassword)) {
            // Increment visit count
            $visitCount += 1;

            // Update Visit_Count and Last_Visited
            $updateStmt = mysqli_prepare($conn, "UPDATE user_details SET Visit_Count = ?, Last_Visited = NOW() WHERE Id = ?");
            mysqli_stmt_bind_param($updateStmt, "ii", $visitCount, $id);
            mysqli_stmt_execute($updateStmt);
            mysqli_stmt_close($updateStmt);

            // Set session
            $_SESSION['user_id'] = $id;
            $_SESSION['username'] = $usernameFetched;

            // Redirect to dashboard
            header("Location: ../dashboard.php");
            exit;
        } else {
            echo "Incorrect password!";
        }
    } else {
        echo "User not found!";
    }
}

mysqli_close($conn);
?>
