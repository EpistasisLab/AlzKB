/*!
* Start Bootstrap - Creative v7.0.6 (https://startbootstrap.com/theme/creative)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
*/
//
// Scripts
//

window.addEventListener('DOMContentLoaded', event => {
  // Navbar shrink function
  const navbarShrink = function () {
    const navbarCollapsible = document.body.querySelector('#mainNav')
    if (!navbarCollapsible) {
      return
    }
    if (window.scrollY === 0) {
      navbarCollapsible.classList.remove('navbar-shrink')
    } else {
      navbarCollapsible.classList.add('navbar-shrink')
    }
  }

  // Shrink the navbar
  navbarShrink()

  // Shrink the navbar when page is scrolled
  document.addEventListener('scroll', navbarShrink)

  // Activate Bootstrap scrollspy on the main nav element
  const mainNav = document.body.querySelector('#mainNav')
  if (mainNav) {
    new bootstrap.ScrollSpy(document.body, {
      target: '#mainNav',
      offset: 74
    })
  }

  // Collapse responsive navbar when toggler is visible
  const navbarToggler = document.body.querySelector('.navbar-toggler')
  const responsiveNavItems = [].slice.call(
    document.querySelectorAll('#navbarResponsive .nav-link')
  )
  responsiveNavItems.map(function (responsiveNavItem) {
    responsiveNavItem.addEventListener('click', () => {
      if (window.getComputedStyle(navbarToggler).display !== 'none') {
        navbarToggler.click()
      }
    })
  })

  // Activate SimpleLightbox plugin for portfolio items
  new SimpleLightbox ({
    elements: '#portfolio a.portfolio-box'
  })
})

function myAccFunc () {
  let x = document.getElementById('doc_sidebar')
  if (x.className.indexOf('w3-show') == -1) {
    x.className += ' w3-show'
    x.previousElementSibling.className += ' w3-green'
  } else {
    x.className = x.className.replace(' w3-show', '')
    x.previousElementSibling.className =
      x.previousElementSibling.className.replace(' w3-green', '')
  }
}

function w3_open () {
  document.getElementById('mySidebar').style.display = 'block'
}

function w3_close () {
  document.getElementById('mySidebar').style.display = 'none'
}
