<?php
session_start();
include "config/db.php"; // correct path

// Example: fetch logged-in user
$user_id = $_SESSION['user_id'] ?? 0;

if ($user_id) {
    $stmt = mysqli_prepare($conn, "SELECT User_Name, email, Last_Visited FROM user_details WHERE ID = ?");
    mysqli_stmt_bind_param($stmt, "i", $user_id);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);

    if ($row = mysqli_fetch_assoc($result)) {
        echo "Welcome, " . $row['User_Name'];
        echo "<br>Email: " . $row['email'];
        echo "<br>Last Visited: " . $row['Last_Visited'];
    } else {
        echo "User not found.";
    }
} else {
    echo "Please login first.";
}
?>
