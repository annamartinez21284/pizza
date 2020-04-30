function load_basket () {
  if (localStorage.getItem("preselection") != null) {
    preselection = localStorage.getItem("preselection");
    console.log("THIS IS PREBASKET JS ", preselection);
    document.querySelector('#test').innerHTML = preselection;
    // do properly - looping thru preselection and building HTML elements 1 by 1
    // have a hidden HTML element on prebasket.html with all the Toppings
    // if pizza add dropdown(s) for each topping in element created
    // check for cheese, 0top, 1top etc to determine # of topping dropdown lists
  }

}



document.addEventListener('DOMContentLoaded', () => {
  load_basket();
})
