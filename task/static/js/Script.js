window.onload = function(){
  var labelRadio = document.querySelectorAll(".labelRadio"),
      error = document.querySelector(".error");

  function onChangeBackgroundClick(){
    for(var i = 0; i < 3; i++){
      labelRadio[i].classList.remove("click");
    }
    this.classList.add("click");
  }

  labelRadio.forEach(click => click.addEventListener("click", onChangeBackgroundClick));

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
