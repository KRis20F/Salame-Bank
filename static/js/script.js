let $ = document.querySelector.bind(document);

window.onload = () => {
    // autorefresh navigator
    setTimeout(() => location.reload('True'),10000);
    $('#menu').onclick = () => {                $('body').classList.toggle('active'); //set class magic animation
    console.log('click');
    }
}