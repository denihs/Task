window.onload = function(){

  var labelRadio = document.querySelectorAll(".labelRadio"),
      error = document.querySelector(".error"),

      iconUser = document.querySelector(".user"),
      menuDeslizante = document.querySelector(".menu-deslizante"),

      removerClose = document.querySelectorAll(".removerClose"),
      corpoExclusao = document.querySelector(".corpo_exclusao"),

      entrada = document.querySelector("#entrada"),
      tarefas = document.querySelectorAll("td"),
      showSearch = document.querySelector(".span_search");

//Efeito nos botões de prioridade
  function onChangeBackgroundClick(){
    for(var i = 0; i < 3; i++){
      labelRadio[i].classList.remove("click");
    }
    this.classList.add("click");
  }
  labelRadio.forEach(click => click.addEventListener("click", onChangeBackgroundClick));

  //Menu deslizante
  function onDropMenuClick(){
    menuDeslizante.classList.toggle("showMenuDeslizante");
  }
  iconUser.addEventListener("click", onDropMenuClick);


  //Cancelar exclusão de uma tarefa
  function onDeleteTaskClick(){
    corpoExclusao.classList.toggle("remover");
  }
  removerClose.forEach(btn => btn.addEventListener("click", onDeleteTaskClick))
if(window.location.pathname == "/tarefas/"){
    //Pesquisa em tempo real
    function onSaidaKeyDown(){
      tarefas.forEach(tarefa => {
          tarefaText = tarefa.textContent.toLowerCase();
          valorPesquisa = entrada.value.toLowerCase();
          if ( tarefaText.indexOf(valorPesquisa) != -1 ){
            tarefa.parentNode.classList.remove("hidden")
          } else{
            tarefa.parentNode.classList.add("hidden")
          }
        })
    }
    entrada.addEventListener("keyup", onSaidaKeyDown)


    showSearch.addEventListener("click", function(e){
          e.preventDefault();
          entrada.classList.toggle("showSearch");
    });
  }
  //Mudar foto de perfil
  if(window.location.pathname == "/perfil/"){
    const inputFile = document.querySelector("#id_image");
    const form  = document.querySelector("form")
    function lidarInputFileClick(e){
      console.log(inputFile);
      form.submit()
    }

    inputFile.addEventListener("change", lidarInputFileClick)
  }
  //Efeito para quando existe um erro
  error.classList.add("show_error");
  setInterval(function(){
    if (error.parentNode) {
      error.parentNode.removeChild(error);
    }
  }, 2500);
  setInterval(function(){
      error.classList.add("remove_error");
    }, 2000);

};
