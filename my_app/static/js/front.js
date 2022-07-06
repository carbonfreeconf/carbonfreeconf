// ---------------------------------------------- //
// Add class 'scrolled' to header on scroll
// ---------------------------------------------- //
window.onload = function() {scrollFunction()};
window.onscroll = function() {scrollFunction()};
let header = document.getElementsByClassName("header")[0];
function scrollFunction() {
  if (document.body.scrollTop > 0 || document.documentElement.scrollTop > 0) {
    header.classList.add("scrolled");
  } else {
    header.classList.remove("scrolled");
  }
}

// ---------------------------------------------- //
// Responsive navbar with hamburger and overlay
// ---------------------------------------------- //
let navResponsive = document.getElementsByClassName("nav-links")[0];
let hamburgerMenu = document.getElementsByClassName("hamburger")[0];
let overlayMenu = document.getElementsByClassName("overlay")[0];
hamburgerMenu.addEventListener("click", function() {
  navResponsive.classList.toggle("open");
  overlayMenu.classList.toggle("appear");
  this.classList.toggle("isOpened");
});
overlayMenu.addEventListener("click", function() {
  navResponsive.classList.remove("open");
  this.classList.remove("appear");
  hamburgerMenu.classList.remove("isOpened");
});

// ---------------------------------------------- //
// Tabs
// ---------------------------------------------- //
function openTab(evt, tabName) {
  let i, x, tablinks;
  x = document.getElementsByClassName("tab");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tabs-link");
  for (i = 0; i < x.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "grid";
  evt.currentTarget.className += " active";
}

// ---------------------------------------------- //
// Scroll to a container function | About Page
// ---------------------------------------------- //
function scrollToContainer() {
  const element = document.getElementById("scrollTarget");
  const yOffset = -75;
  const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
  window.scrollTo({ top: y, behavior: 'smooth' });
}

// ---------------------------------------------- //
// Scroll to a container function | Blog Page
// ---------------------------------------------- //
function scrollToContainerBis() {
  const element = document.getElementById("scrollTargetBis");
  const yOffset = -75;
  const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
  window.scrollTo({ top: y, behavior: 'smooth' });
}

// ---------------------------------------------- //
// Navbar dropdown
// ---------------------------------------------- //
let btn = document.getElementById("signIn");
let dropdown = document.getElementById("dropdown");
//alert('drop'+btn);
if (btn!=null){
btn.addEventListener("click", function() {
  dropdown.classList.toggle("opened");
});
window.addEventListener("click", function(e) {
  if (!dropdown.contains(e.target) && (!btn.contains(e.target))) {
    dropdown.classList.remove("opened");
  }
});
}
