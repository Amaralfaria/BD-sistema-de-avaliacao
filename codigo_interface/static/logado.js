usuario = localStorage.getItem("matricula");
if(usuario!=null){
    meu_perfil = document.getElementById("meu_perfil");
    meu_perfil.style.display = "";
    link_meu_perfil = document.querySelector("#meu_perfil a");
    link_meu_perfil.href += usuario;

    autorizacao = localStorage.getItem("autorizacao");
    if(autorizacao != null && autorizacao.toLowerCase() == "administrador"){
        link_denuncias = document.getElementById("denuncias");
        link_denuncias.style.display = "";
    }

}

// matricula = document.getElementById("matricula");


// if(matricula.innerText != "" && localStorage.getItem("matricula") == null){
//     localStorage.setItem("matricula", matricula.innerText)
// }






