const toggleDiv = document.querySelector(".mobile__menuoverlay");
const closeBtn = document.querySelector(".closebtn");
const showSidebar = document.querySelector(".mobile__menubtn");

closeBtn.addEventListener("click", function () {
  toggleDiv.classList.remove("toggle__sidebar");
});

showSidebar.addEventListener("click", function () {
  toggleDiv.classList.add("toggle__sidebar");
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

document.addEventListener('DOMContentLoaded', () => {
  const counters = document.querySelectorAll('.stats-number');

  // Optional: log to confirm elements are found
  console.log('Found counters:', counters.length);

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        counters.forEach(counter => {
          const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            let count = +counter.innerText.replace('+', ''); // remove + if present
            const increment = target / 150; // adjust speed (smaller = faster)

            if (count < target) {
              count += increment;
              counter.innerText = Math.ceil(count) + (target > 10 ? '+' : '');
              setTimeout(updateCount, 12); // slightly slower for smoothness
            } else {
              counter.innerText = target + (target > 10 ? '+' : '');
            }
          };
          updateCount();
        });

        // Stop observing once animation is done
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.3,         // start animation when 30% visible
    rootMargin: '0px'       // optional: adjust if needed
  });

  // Observe the banner itself (or any parent that contains it)
  const statsBanner = document.querySelector('.stats-banner');
  if (statsBanner) {
    observer.observe(statsBanner);
  } else {
    console.warn('Stats banner element not found');
  }
});
