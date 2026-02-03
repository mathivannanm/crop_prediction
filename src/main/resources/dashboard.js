/* ================= MENU TOGGLE ================= */
const menuBtn = document.querySelector(".menu-btn");
const menuOverlay = document.querySelector(".menu-overlay");
const menuCard = document.querySelector(".menu-card");

menuBtn.addEventListener("click", () => {
    menuOverlay.classList.toggle("active");
    menuCard.classList.toggle("active");
});

menuOverlay.addEventListener("click", () => {
    menuOverlay.classList.remove("active");
    menuCard.classList.remove("active");
});


/* ================= SLIDER ================= */
const slides = document.querySelectorAll(".slide");
const dotsContainer = document.querySelector(".slider-dots");

let currentSlide = 0;
let slideInterval;

/* ---- CLEAR OLD DOTS (IMPORTANT FIX) ---- */
dotsContainer.innerHTML = "";

/* ---- CREATE DOTS (MATCH SLIDES COUNT) ---- */
slides.forEach((slide, index) => {
    const dot = document.createElement("span");
    dot.classList.add("dot");

    if (index === 0) dot.classList.add("active");

    dot.addEventListener("click", () => {
        showSlide(index);
        resetInterval();
    });

    dotsContainer.appendChild(dot);
});

const dots = document.querySelectorAll(".dot");

/* ---- SHOW SLIDE ---- */
function showSlide(index) {
    slides.forEach(slide => slide.classList.remove("active"));
    dots.forEach(dot => dot.classList.remove("active"));

    slides[index].classList.add("active");
    dots[index].classList.add("active");

    currentSlide = index;
}

/* ---- NEXT SLIDE ---- */
function nextSlide() {
    let next = currentSlide + 1;
    if (next >= slides.length) next = 0;
    showSlide(next);
}

/* ---- AUTO PLAY ---- */
function startSlider() {
    slideInterval = setInterval(nextSlide, 3500);
}

/* ---- RESET TIMER ---- */
function resetInterval() {
    clearInterval(slideInterval);
    startSlider();
}

/* ---- START SLIDER ---- */
showSlide(0);
startSlider();


/* ================= MOBILE SWIPE ================= */
let startX = 0;
let endX = 0;
const slider = document.querySelector(".slider");

slider.addEventListener("touchstart", e => {
    startX = e.touches[0].clientX;
});

slider.addEventListener("touchend", e => {
    endX = e.changedTouches[0].clientX;

    if (startX - endX > 50) nextSlide(); // swipe left

    if (endX - startX > 50) {
        let prev = currentSlide - 1;
        if (prev < 0) prev = slides.length - 1;
        showSlide(prev);
    }
    resetInterval();
});


/* ================= GALLERY SHOW MORE ================= */
let galleryIndex = 5;

function showMore() {
    const gallery = document.querySelector(".gallery-cards");

    for (let i = 0; i < 4; i++) {
        const card = document.createElement("div");
        card.className = "card";

        const img = document.createElement("img");
        img.src = `assets/images/gallery${galleryIndex}.jpg`;
        img.alt = "Gallery Image";

        card.appendChild(img);
        gallery.appendChild(card);

        galleryIndex++;
    }
}
