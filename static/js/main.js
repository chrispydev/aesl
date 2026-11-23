document.addEventListener("DOMContentLoaded", () => {

  // Newsletter subscription
  const newsletterForms = document.querySelectorAll("[data-newsletter-form]");
  newsletterForms.forEach((form) => {
    const messageEl = form.querySelector(".footer__newsletter-message");
    const button = form.querySelector('button[type="submit"]');
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (messageEl) {
        messageEl.textContent = "Subscribing...";
        messageEl.classList.remove("is-error", "is-success");
      }
      if (button) button.disabled = true;
      try {
        const res = await fetch(form.action, {
          method: "POST",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]")?.value || "",
          },
          body: new FormData(form),
        });
        const data = await res.json().catch(() => ({}));
        const ok = res.ok && data.ok;
        if (messageEl) {
          messageEl.textContent = data.message || (ok ? "Subscribed." : "Subscription failed.");
          messageEl.classList.toggle("is-success", !!ok);
          messageEl.classList.toggle("is-error", !ok);
        }
        if (ok) form.reset();
      } catch {
        if (messageEl) {
          messageEl.textContent = "Subscription failed. Please try again.";
          messageEl.classList.add("is-error");
        }
      } finally {
        if (button) button.disabled = false;
      }
    });
  });


  /* =========================
     MOBILE MENU TOGGLE
  ========================== */

  const toggleDiv = document.querySelector(".mobile__menuoverlay");
  const closeBtn = document.querySelector(".closebtn");
  const showSidebar = document.querySelector(".mobile__menubtn");

  const closeMobileMenu = () => {
    if (!toggleDiv) return;
    toggleDiv.classList.remove("toggle__sidebar");
    toggleDiv.setAttribute("aria-hidden", "true");
    if (showSidebar) showSidebar.setAttribute("aria-expanded", "false");
    document.body.classList.remove("mobile-menu-open");
  };

  const openMobileMenu = () => {
    if (!toggleDiv) return;
    toggleDiv.classList.add("toggle__sidebar");
    toggleDiv.setAttribute("aria-hidden", "false");
    if (showSidebar) showSidebar.setAttribute("aria-expanded", "true");
    document.body.classList.add("mobile-menu-open");
  };

  if (closeBtn) {
    closeBtn.addEventListener("click", closeMobileMenu);
  }

  if (showSidebar) {
    showSidebar.addEventListener("click", openMobileMenu);
  }

  if (toggleDiv) {
    toggleDiv.addEventListener("click", (event) => {
      if (event.target === toggleDiv) closeMobileMenu();
    });

    toggleDiv.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", closeMobileMenu);
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && toggleDiv.classList.contains("toggle__sidebar")) {
        closeMobileMenu();
      }
    });
  }




  // ==============================
  // NAVBAR LIVE SEARCH
  // ==============================

  const searchInputs = document.querySelectorAll(".search__input");
  const searchResultsContainers = document.querySelectorAll(".search__results-container");

  searchInputs.forEach((input, index) => {

    const searchResults = searchResultsContainers[index];

    let searchTimeout;

    input.addEventListener("input", function () {

      const query = this.value.trim();

      clearTimeout(searchTimeout);

      if (query.length < 1) {

        searchResults.innerHTML = "";
        searchResults.style.display = "none";
        return;

      }

      searchTimeout = setTimeout(async () => {

        try {

          const response = await fetch(
            `/api/search/?q=${encodeURIComponent(query)}`
          );

          const data = await response.json();

          searchResults.innerHTML = "";

          if (!data.results || data.results.length === 0) {

            searchResults.innerHTML = `
            <div class="search__item">
              No results found
            </div>
          `;

            searchResults.style.display = "block";
            return;

          }

          data.results.forEach(item => {

            let icon = "";

            if (item.type === "person") {

              icon = `<i class="fas fa-user"></i>`;

            }
            else if (item.type === "project") {

              icon = `<i class="fas fa-building"></i>`;

            }
            else if (item.type === "project_category") {

              icon = `<i class="fas fa-layer-group"></i>`;

            }

            const resultItem = document.createElement("div");

            resultItem.classList.add("search__item");

            resultItem.setAttribute("data-url", item.url);

            resultItem.innerHTML = `
            <div class="search__result-title">
              ${icon}
              <strong>${item.name}</strong>
            </div>

            <small>
              ${item.subtitle || item.type}
            </small>
          `;

            resultItem.addEventListener("click", () => {

              if (item.url) {
                window.location.href = item.url;
              }

            });

            searchResults.appendChild(resultItem);

          });

          searchResults.style.display = "block";

        }
        catch (error) {

          console.error("Search error:", error);

        }

      }, 300);

    });

    // Show results when focusing the input
    input.addEventListener("focus", function () {

      if (searchResults.innerHTML.trim()) {
        searchResults.style.display = "block";
      }

    });

  });

  // Hide all dropdowns when clicking outside
  document.addEventListener("click", function (event) {

    if (!event.target.closest(".search__container")) {

      searchResultsContainers.forEach(container => {

        container.style.display = "none";

      });

    }

  });







  /* =========================
     SIDENAV SCROLL BEHAVIOR
  ========================== */


  const sideNav = document.querySelector(".sector__aside");
  const footer = document.querySelector(".site__footer");
  const triggerPoint = 600;


  let footerVisible = false;



  if (sideNav) {


    window.addEventListener(
      "scroll",
      () => {


        if (
          window.scrollY >= triggerPoint &&
          !footerVisible
        ) {


          sideNav.classList.add("active");


        }
        else {


          sideNav.classList.remove("active");


        }


      }
    );


  }






  /* =========================
     FOOTER INTERSECTION OBSERVER
  ========================== */


  if (sideNav && footer) {


    const footerObserver =
      new IntersectionObserver(
        (entries) => {


          entries.forEach(entry => {


            footerVisible =
              entry.isIntersecting;



            if (footerVisible) {

              sideNav.classList.remove(
                "active"
              );

            }


          });


        },
        {
          root: null,
          threshold: 0.1,
        }
      );



    footerObserver.observe(
      footer
    );


  }








  /* =========================
     STATS COUNTER ANIMATION
  ========================== */


  const counters =
    document.querySelectorAll(
      ".stats-number"
    );


  const statsBanner =
    document.querySelector(
      ".stats-banner"
    );



  if (
    counters.length > 0 &&
    statsBanner
  ) {


    const formatNumber = (num) => {


      if (num >= 1000) {

        return (
          Math.floor(num / 1000)
          + "k+"
        );

      }


      return num + "+";


    };




    const statsObserver =
      new IntersectionObserver(
        (entries, observer) => {


          entries.forEach(entry => {


            if (entry.isIntersecting) {



              counters.forEach(counter => {


                const target =
                  parseInt(
                    counter.getAttribute(
                      "data-target"
                    )
                  ) || 0;



                let count = 0;



                const duration = 2000;

                const frameRate = 16;

                const totalSteps =
                  duration / frameRate;


                const increment =
                  target / totalSteps;




                const updateCount = () => {


                  count += increment;



                  if (count < target) {


                    counter.innerText =
                      formatNumber(
                        Math.floor(count)
                      );


                    requestAnimationFrame(
                      updateCount
                    );


                  }
                  else {


                    counter.innerText =
                      formatNumber(
                        target
                      );


                  }


                };



                updateCount();



              });



              observer.unobserve(
                entry.target
              );


            }



          });



        },
        {
          threshold: 0.3
        }
      );



    statsObserver.observe(
      statsBanner
    );


  }







  /* =========================
     SWIPER JS INITIALIZATION
  ========================== */


  if (document.querySelector(".swiper")) {


    new Swiper('.swiper', {


      loop: true,


      autoplay: {


        delay: 5000,

        disableOnInteraction: false,


      },


      effect: 'fade',


      fadeEffect: {


        crossFade: true


      },


      pagination: {


        el: '.swiper-pagination',

        clickable: true,


      },


    });


  }



});
