let slideIndex = 0;

function showSlides() {
    const slides = document.querySelectorAll('.slide');
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none"; // Скрыть все слайды
    }
    slideIndex++;
    if (slideIndex > slides.length) { slideIndex = 1 } // Переключение на первый слайд
    slides[slideIndex - 1].style.display = "block"; // Показать текущий слайд
}

// Переключение слайдов по кнопкам
function changeSlide(n) {
    slideIndex += n; // Изменить индекс слайда
    const slides = document.querySelectorAll('.slide');
    if (slideIndex > slides.length) { slideIndex = 1; }
    if (slideIndex < 1) { slideIndex = slides.length; }
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none"; // Скрыть все слайды
    }
    slides[slideIndex - 1].style.display = "block"; // Показать текущий слайд
}

// Инициализация слайдера
document.addEventListener('DOMContentLoaded', function () {
    showSlides(); // Показать первый слайд
});
