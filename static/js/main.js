document.addEventListener("DOMContentLoaded", () => {

  /* =========================
     MOBILE MENU TOGGLE
  ========================== */

  const toggleDiv = document.querySelector(".mobile__menuoverlay");
  const closeBtn = document.querySelector(".closebtn");
  const showSidebar = document.querySelector(".mobile__menubtn");

  if (toggleDiv && closeBtn) {
    closeBtn.addEventListener("click", () => {
      toggleDiv.classList.remove("toggle__sidebar");
    });
  }

  if (toggleDiv && showSidebar) {
    showSidebar.addEventListener("click", () => {
      toggleDiv.classList.add("toggle__sidebar");
    });
  }


  /* =========================
     SIDENAV SCROLL BEHAVIOR
  ========================== */

  const sideNav = document.querySelector(".sector__aside");
  const footer = document.querySelector(".site__footer");
  const triggerPoint = 600;

  let footerVisible = false;

  if (sideNav) {
    window.addEventListener("scroll", () => {
      if (window.scrollY >= triggerPoint && !footerVisible) {
        sideNav.classList.add("active");
      } else {
        sideNav.classList.remove("active");
      }
    });
  }


  /* =========================
     FOOTER INTERSECTION OBSERVER
  ========================== */

  if (sideNav && footer) {
    const footerObserver = new IntersectionObserver(
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
      }
    );

    footerObserver.observe(footer);
  }


  /* =========================
     STATS COUNTER ANIMATION
  ========================== */

  const counters = document.querySelectorAll(".stats-number");
  const statsBanner = document.querySelector(".stats-banner");

  if (counters.length > 0 && statsBanner) {

    const formatNumber = (num) => {
      if (num >= 1000) {
        return Math.floor(num / 1000) + "k+";
      }
      return num + "+";
    };
    const statsObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {

        if (entry.isIntersecting) {

          counters.forEach(counter => {
            const target = parseInt(counter.getAttribute("data-target")) || 0;
            let count = 0;

            const duration = 2000;
            const frameRate = 16;
            const totalSteps = duration / frameRate;
            const increment = target / totalSteps;

            const updateCount = () => {
              count += increment;

              if (count < target) {
                counter.innerText = formatNumber(Math.floor(count));
                requestAnimationFrame(updateCount);
              } else {
                counter.innerText = formatNumber(target);
              }
            };

            updateCount();
          });

          observer.unobserve(entry.target);
        }

      });
    }, {
      threshold: 0.3
    });

    statsObserver.observe(statsBanner);
  }


  // =========================
  // SWIPER JS INITIALIZATION
  const swiper = new Swiper('.swiper', {
    loop: true,
    autoplay: {
      delay: 5000, // 5 seconds per slide
      disableOnInteraction: false,
    },
    effect: 'fade', // smooth fade transition
    fadeEffect: {
      crossFade: true
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
  });

});

