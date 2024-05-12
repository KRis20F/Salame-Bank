const navHeader = document.querySelector('#nav-header');
const openButtom = document.querySelector('#open-bar');
const closeButtom = document.querySelector('#close-bar');

const btnLeft = document.querySelector('#btn-left'),
      btnRight = document.querySelector('#btn-next'), // Corregido el nombre de la variable
      slider = document.querySelector('#slider-hero'),
      sliderSection = document.querySelectorAll('.img-carrusel');

btnLeft.addEventListener("click", e => moveToLeft());
btnRight.addEventListener("click", e => moveToRight()); // Corregido el nombre de la función

setInterval(() => {
    moveToRight();
},7000)

let operacion = 0,
    counter = 0,
    widthImg = 326 / sliderSection.length;

function moveToRight() {
    if (counter >= sliderSection.length - 1)
    {
        counter = 0;
        operacion = 0;
        slider.style.transform = `translate(-${operacion}%)`;
    }

    else
    {
        counter++
        console.log(counter);
        operacion = operacion + widthImg;
        slider.style.transform = `translate(-${operacion}%)`; // Utilizando comillas invertidas graves para la interpolación
        slider.style.transition = "all ease .6s";
    }
}

function moveToLeft() {
    counter--;
    if (counter < 0 ) {
        counter = sliderSection.length - 1;
        operacion = widthImg * (sliderSection.length - 1)
        console.log(operacion);
        slider.style.transform = `translate(-${operacion}%)`;
    }

    else 
    {
        operacion = operacion - widthImg;
        slider.style.transform = `translate(-${operacion}%)`; // Utilizando comillas invertidas graves para la interpolación
        slider.style.transition = "all ease .6s";
    }
}

openButtom.addEventListener("click", () => {
    navHeader.classList.add("visible");
})

closeButtom.addEventListener("click", () => {
    navHeader.classList.remove("visible");
})


