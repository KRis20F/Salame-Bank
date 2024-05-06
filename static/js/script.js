const navHeader = document.querySelector('#nav-header');
const openButtom = document.querySelector('#open-bar');
const closeButtom = document.querySelector('#close-bar');

openButtom.addEventListener("click", () => {
    navHeader.classList.add("visible");
})

closeButtom.addEventListener("click", () => {
    navHeader.classList.remove("visible");
})



//animacion entre paginas webs

barba.init({
    transition: [{
        name: 'prueba',
        leave: function(data) {
            var done = this.async();
            document.body.classList.add('loading');
            setTimeout(function(){
                done();
            },900);
        },
        enter:
        function(data) {
            var done = this.async();
            document.body.classList.add('loading');
            setTimeout(function(){
                done();
            },900);
        }
    }]
})

// Abrir menu en modo telefono



