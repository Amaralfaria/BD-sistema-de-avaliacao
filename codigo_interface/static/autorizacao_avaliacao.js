window.onload = function(){
    cards = document.getElementsByClassName("card-comentario");
    matricula_usuario = localStorage.getItem("matricula");
    
    for(let i = 0;i<cards.length;i++){
        btns = cards[i].getElementsByClassName("btn_usuario_especifico");
        matricula = cards[i].getElementsByClassName("matricula_comentario")[0].innerText;
        if(matricula!=matricula_usuario){
            btns[0].style.display = "none"
            btns[1].style.display = "none"
        }
        
    }




    

}