
function navbarBurgerClicked()
{
    // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      $(".navbar-burger").toggleClass("is-active");
      $(".navbar-menu").toggleClass("is-active");
}

function documentReady()
{
    $(".navbar-burger").click(navbarBurgerClicked);

    document.body.addEventListener('htmx:configRequest', (event) => {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        if (csrfToken) {
            event.detail.headers['X-CSRFToken'] = csrfToken;
        }
    });
}

$(document).ready(documentReady);
