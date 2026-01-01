const toggleDiv = document.querySelector(".mobile__menuoverlay");
const closeBtn = document.querySelector(".closebtn");
const showSidebar = document.querySelector(".mobile__menubtn");

closeBtn.addEventListener("click", function () {
    toggleDiv.classList.remove("toggle__sidebar");
});

showSidebar.addEventListener("click", function () {
    toggleDiv.classList.add("toggle__sidebar");
});

const galleryItems = document.querySelectorAll(".projects__image");
galleryItems.forEach((item) => {
    const rowHeight = parseInt(
        window
            .getComputedStyle(
                document.querySelector(".projects__masonry-gallery"),
            )
            .getPropertyValue("grid-auto-rows"),
    );
    const rowGap = parseInt(
        window
            .getComputedStyle(
                document.querySelector(".projects__masonry-gallery"),
            )
            .getPropertyValue("gap"),
    );
    const imgHeight = item.querySelector("img").getBoundingClientRect().height;
    const rowSpan = Math.ceil((imgHeight + rowGap) / (rowHeight + rowGap));
    item.style.gridRowEnd = `span ${rowSpan}`;
});

const sideNav = document.querySelector(".sector__aside");
const footer = document.querySelector(".site__footer");
const triggerPoint = 600;

let footerVisible = false;

window.addEventListener("scroll", () => {
    if (window.scrollY >= triggerPoint && !footerVisible) {
        sideNav.classList.add("active");
    } else {
        sideNav.classList.remove("active");
    }
});

// Observe footer
const observer = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            footerVisible = entry.isIntersecting;

            if (footerVisible) {
                sideNav.classList.remove("active");
            }
        });
    },
    {
        root: null,
        threshold: 0.1,
    },
);

observer.observe(footer);
