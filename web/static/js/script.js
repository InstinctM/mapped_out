var slideIndex = 1;
showSlides(slideIndex);
function plusSlides(n) {
    showSlides(slideIndex += n);
}
function currentSlide(n) {
    showSlides(slideIndex = n);
}
function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
    if (n > slides.length) {
        slideIndex = 1
    }
    if (n < 1) {
        slideIndex = slides.length
    }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}

function hideCookiePrompt() {
    localStorage.setItem("cookie-accept", true);
    document.getElementById("cookie-prompt").style.display = "none";
}

// Check cookie consent
document.addEventListener("scroll", (e) => {
    console.log(this.scrollY, document.documentElement.clientHeight);
    // only show when scrolled down
    if (this.scrollY > document.documentElement.clientHeight) {
        let cookieAccept = localStorage.getItem("cookie-accept");
        if (cookieAccept == null) {
            document.getElementById("cookie-prompt").style.display = "block";
        }
    } else {
        document.getElementById("cookie-prompt").style.display = "none";
    }
});
