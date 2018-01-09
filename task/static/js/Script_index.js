window.onload = function(){
    const  btnLogin = document.querySelector(".btn-login"),
           formDeslizante = document.querySelector("header"),
           error = document.querySelector(".error");

    //Menu deslizante
    function onDropMenuClick(){
      formDeslizante.classList.toggle("showMenuDeslizante");
    }
    btnLogin.addEventListener("click", onDropMenuClick);

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
