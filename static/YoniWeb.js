const activePage = window.location.pathname;
console.log(window);
console.log(window.location);
console.log(activePage);

/*create an arey of the links in nav,
compare each to pathname and mark the one that is active
*/
const navLinks = document.querySelectorAll('nav a').forEach(link => {
  if(link.href.includes(`${activePage}`)){
    link.classList.add('active');
  }
});
const sundImg = document.getElementById("imgM");
const TextDiv = document.getElementById("textDiv");
TextDiv.addEventListener("mouseover",BoldBorder);
TextDiv.addEventListener("mouseout",BoldBorderOut);

function BoldBorder(){
  TextDiv.style.WebkitBorderImage= "linear-gradient(to left, rgba(172, 199, 225, 0.4), rgb(27, 39, 69)) 1 0 ";

}
function BoldBorderOut(){
  TextDiv.style.WebkitBorderImage= "";

}

function rotate(){


  sundImg.style.visibility="visible";

  setTimeout(function(){sundImg.style.visibility="hidden"; } ,5000);
}
