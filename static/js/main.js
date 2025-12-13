const toggleDiv = document.querySelector(".mobile__menuoverlay");
const closeBtn = document.querySelector(".closebtn");
const showSidebar = document.querySelector(".mobile__menubtn")


closeBtn.addEventListener("click", function () {
  toggleDiv.classList.remove('toggle__sidebar')

});

showSidebar.addEventListener("click", function () {
  toggleDiv.classList.add('toggle__sidebar')
})




