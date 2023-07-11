matricula = document.getElementById("matricula");
numero_matricula = localStorage.getItem("matricula");
matricula.value = numero_matricula;

btn_denuncia = document.getElementsByClassName("denuncia");

for(let i = 0; i< btn_denuncia.length;i++){
    btn_denuncia[i].href += numero_matricula;
}


// if(numero_matricula != null){

// }
