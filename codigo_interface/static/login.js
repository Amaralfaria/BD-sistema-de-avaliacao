matricula = document.getElementById("matricula");

if(matricula.innerText != localStorage.getItem("matricula")){
    autorizacao = document.getElementById("autorizacao")
    localStorage.setItem("matricula", matricula.innerText)
    localStorage.setItem("autorizacao", autorizacao.innerText)
}

btn_deletar = document.getElementById("btn_deletar");
btn_deletar.onclick = function(){
    localStorage.clear();
}



const urlCreator = window.URL || window.webkitURL;
foto_perfil = document.getElementById('foto_perfil');
data = foto_perfil.src;
foto_perfil.src = urlCreator.createObjectURL(data);
