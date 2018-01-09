window.onload = function(){
  var error = document.querySelector(".error");

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
