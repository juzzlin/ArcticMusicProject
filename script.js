document.addEventListener('scroll', function() {
    const heroImage = document.querySelector('header');
    const scrollPosition = window.scrollY;

    // The '0.5' value determines the speed of the parallax effect.
    // A smaller value makes it move slower.
    heroImage.style.backgroundPositionY = `${scrollPosition * 0.5}px`;
});
