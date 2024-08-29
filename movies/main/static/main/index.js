
document.addEventListener("DOMContentLoaded",()=>{
      document.querySelector(".example").onsubmit = get_movie;
});

function get_movie(){

    const input = document.forms["movie_search"]["search"].value;

    if(input == ""){
        alert("Input is not provided");
        return false;
    }
  
}