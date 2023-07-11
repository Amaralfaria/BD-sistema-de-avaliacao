window.onload = function(){
    autorizacao = localStorage.getItem("autorizacao");
    if(autorizacao == null || autorizacao.toLowerCase() != "administrador"){
        btn_criar = document.getElementById("cria_turma");
        btns_deletar = document.getElementsByClassName("altera_turma");

        btn_criar.style.display = "none";
        for(let i = 0;i<btns_deletar.length;i++){
            btns_deletar[i].style.display = "none";
        }
    }
}