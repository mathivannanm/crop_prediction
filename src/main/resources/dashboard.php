<?php
session_start();

if(!isset($_SESSION['user_name'])){
    header("Location: index.php");
    exit();
}

$username = $_SESSION['user_name'];
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <!-- Correct CSS path -->
    <link rel="stylesheet" href="css/dashboard.css">
</head>
<body>

<!-- ===== TOP BAR ===== -->
<div class="top-bar">
    <button class="menu-btn">&#9776;</button>
    <div class="top-right">
        <span class="user-name"><?php echo htmlspecialchars($username); ?></span>
        <div class="profile">👤</div>
    </div>
</div>

<!-- ===== SIDE MENU ===== -->
<div class="menu-overlay"></div>
<div class="menu-card">
    <a href="#home">Home</a>
    <a href="#galleryId">Gallery</a>
    <a href="#location">Location</a>
    <a href="#feedback">Feedback</a>
    <a href="logout.php">Logout</a>
</div>

<!-- ===== WELCOME ===== -->
<div class="welcome" id="home">
    <h1>வணக்கம் <?php echo htmlspecialchars($username); ?>!</h1>
    <p>வயலேஈஸ்வரர் ஆலயத்திற்கு உங்கள் வருகையை அன்புடன் வரவேற்கிறோம்</p>
</div>

<!-- ===== SLIDER ===== -->
<div class="slider">
    <div class="slide active">
        <img src="assets/images/slide1.png" alt="Slide 1">
        <div class="caption">Slide Caption 1</div>
    </div>
    <div class="slide">
        <img src="assets/images/slide2.jpg" alt="Slide 2">
        <div class="caption">Slide Caption 2</div>
    </div>
    <div class="slide">
        <img src="assets/images/slide3.jpg" alt="Slide 3">
        <div class="caption">Slide Caption 3</div>
    </div>
    <div class="slide">
        <img src="assets/images/slide4.jpg" alt="Slide 4">
        <div class="caption">Slide Caption 4</div>
    </div>
    <div class="slide">
        <img src="assets/images/slide5.jpg" alt="Slide 5">
        <div class="caption">Slide Caption 5</div>
    </div>
</div>
<div class="slider-dots"></div>

<div class="slider-dots"></div>

<h2 class="section-title" id="galleryId">Gallery</h2>

<div class="gallery-box">

    <!-- Gallery Card Heading -->
    <h3 class="gallery-heading">திருவூடல் திருவிழா நினைவுகள்</h3>

    <div class="gallery-grid">

    <a href="https://drive.google.com/drive/folders/1Uw1_y7-K-LdqjoOOat8L4Ttro__GdsLN"
       target="_blank"
       class="gallery-item glow-1">
        <img src="assets/images/gallery1.jpg" alt="Gallery 1">
        <div class="overlay-text">
            <span class="line-1">1 ஆம் ஆண்டு</span>
            <span class="line-2">திருவிழா</span>
    
</div>

        
    </a>

    <a href="https://drive.google.com/drive/folders/19kvvtHXGJkiGQ9-uHJlq9gczUqiuFQcC"
       target="_blank"
       class="gallery-item glow-2">
        <img src="assets/images/gallery2.jpg" alt="Gallery 2">
        <div class="overlay-text">
    <span class="line-1">2 ஆம் ஆண்டு</span>
    <span class="line-2">திருவிழா</span>
</div>

    </a>

    <a href="https://drive.google.com/drive/folders/1OtJ6VYBLn_US0jbYHKLEc7o8OzHYnWql"
       target="_blank"
       class="gallery-item glow-3">
        <img src="assets/images/gallery3.jpg" alt="Gallery 3">
        <div class="overlay-text">
    <span class="line-1">3 ஆம் ஆண்டு</span>
    <span class="line-2">திருவிழா</span>
</div>

    </a>

    <a href="https://drive.google.com/drive/folders/1dn43YUn_KRWh15BL54AthGjICcsiPA2R"
       target="_blank"
       class="gallery-item glow-4">
        <img src="assets/images/gallery4.jpg" alt="Gallery 4">
        <div class="overlay-text">
    <span class="line-1">4 ஆம் ஆண்டு</span>
    <span class="line-2">திருவிழா</span>
</div>

    </a>
    <a href="https://drive.google.com/drive/folders/1VP1dwBqonh6RzS7u9OkRqMFdzw20MHvK"
       target="_blank"
       class="gallery-item glow-4">
        <img src="assets/images/gallery5.jpg" alt="Gallery 5">
        <div class="overlay-text">
    <span class="line-1">5 ஆம் ஆண்டு</span>
    <span class="line-2">திருவிழா</span>
</div>

    </a>

</div>


    <a class="gallery-btn"
       href="https://drive.google.com/drive/folders/1OyBmWkjuZyhhp6QTGyrixc2vZcHKuoyX"
       target="_blank">
       Show More
    </a>

</div>
<!-- Temple Location Card -->
<div class="location-card" id="location">

    <h2 class="location-title">📍 கோவில் இருப்பிடம்</h2>

    <p class="location-subtitle">
        ஸ்ரீ வயலீஸ்வரர் திருக்கோவில், சித்தாத்தூர்
    </p>

    <div class="map-container">
        <iframe
            src="https://www.google.com/maps?q=12.0169614,79.3033386&z=17&output=embed"
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade">
        </iframe>
    </div>

    <a
        href="https://www.google.com/maps/place/Sithathur/@12.0169614,79.2984677,17z/data=!3m1!4b1!4m9!1m2!2m1!1sVayaleeshwarar+Temple+in+sithatur!3m5!1s0x3bacada156db8587:0xee5b4d910582dc20!8m2!3d12.0169614!4d79.3033386!16s%2Fg%2F11jclvrwhd"
        target="_blank"
        class="map-button">
        Google Map-ல் திறக்க
    </a>

</div>


<div class="feedback-card" id="feedback">
    <h3>உங்கள் கருத்து</h3>

    <form action="#" method="post">
        <input type="text" name="name" placeholder="உங்கள் பெயர் [Name]" required>
        <input type="email" name="email" placeholder="மின்னஞ்சல் [Email]" required>
        <textarea name="message" rows="4" placeholder="உங்கள் கருத்தை பதிவு செய்யவும் [Enter Text]" required></textarea>
        <button type="submit">Submit</button>
    </form>
</div>


</div>

<!-- ===== JS ===== -->
<script src="js/script.js"></script>
</body>
</html>
