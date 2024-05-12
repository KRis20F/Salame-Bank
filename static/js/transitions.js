// animacion entre paginas webs

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