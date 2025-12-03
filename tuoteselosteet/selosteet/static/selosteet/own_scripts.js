/* calculate A4 proportions, and how many lines fit on to one page */
function linesOnPage(css_selector) {
  var width = $('#content').first().width()
  var a4Height = (width / 210) * (297 - 30)

  if ($(css_selector).length > 0) {
    return Math.floor(a4Height / $(css_selector).first().height())
  }
  return 1
}

function _log(x) {
  console.log(x)
}

function getProductHtml(css_selector) {
  var list = document.getElementsByClassName(css_selector)
  if (list.length > 0) return list[0].outerHTML
  return ''
}

// === FAVORITES FUNCTIONALITY ===
function getFavorites() {
  var favorites = localStorage.getItem('productFavorites')
  return favorites ? JSON.parse(favorites) : []
}

function saveFavorites(favorites) {
  localStorage.setItem('productFavorites', JSON.stringify(favorites))
}

function toggleFavorite(productUrl) {
  var favorites = getFavorites()
  var index = favorites.indexOf(productUrl)

  if (index > -1) {
    favorites.splice(index, 1)
  } else {
    favorites.push(productUrl)
  }

  saveFavorites(favorites)
  updateFavoriteStars()
}

function isFavorite(productUrl) {
  return getFavorites().indexOf(productUrl) > -1
}

function updateFavoriteStars() {
  $('.product').each(function () {
    var url = $(this).find('a').attr('href')
    var star = $(this).find('.favorite-star')

    if (isFavorite(url)) {
      star.addClass('active')
    } else {
      star.removeClass('active')
    }
  })
}

function sortProductsByFavorites() {
  var container = $('.content-wrap')
  var products = container.find('.product').detach()
  var favorites = getFavorites()

  // Sort: favorites first, then alphabetically
  products.sort(function (a, b) {
    var urlA = $(a).find('a').attr('href')
    var urlB = $(b).find('a').attr('href')
    var isFavA = favorites.indexOf(urlA) > -1
    var isFavB = favorites.indexOf(urlB) > -1

    if (isFavA && !isFavB) return -1
    if (!isFavA && isFavB) return 1

    var nameA = $(a).find('a').text().trim()
    var nameB = $(b).find('a').text().trim()
    return nameA.localeCompare(nameB, 'fi')
  })

  container.append(products)
}

function initializeFavorites() {
  // Add star icons to each product
  $('.product').each(function () {
    var url = $(this).find('a').attr('href')
    var star = $('<span class="favorite-star" style="cursor: pointer; margin-right: 8px; user-select: none;">★</span>')

    star.on('click', function (e) {
      e.preventDefault()
      toggleFavorite(url)
      if ($('#sort-favorites').hasClass('active')) {
        sortProductsByFavorites()
      }
      return false
    })

    $(this).prepend(star)
  })

  updateFavoriteStars()

  // Add sorting toggle to sidebar menu
  var sortMenuItem = $(
    '<li id="favorites-menu-item">' +
      '<a href="#" id="sort-favorites" style="cursor: pointer;">' +
      '<span class="glyphicon glyphicon-star"></span> ' +
      'Suosikit ensin' +
      '</a>' +
      '</li>'
  )

  // Insert after the "Tuotteet" menu item
  $('.side-menu .navbar-nav li').eq(1).after(sortMenuItem)

  // Check if sorting was enabled before
  var sortEnabled = localStorage.getItem('sortFavoritesEnabled') === 'true'
  if (sortEnabled) {
    $('#sort-favorites').addClass('active')
    sortProductsByFavorites()
  }

  // Toggle sorting
  $('#sort-favorites').on('click', function (e) {
    e.preventDefault()
    $(this).toggleClass('active')
    var isActive = $(this).hasClass('active')
    localStorage.setItem('sortFavoritesEnabled', isActive)

    if (isActive) {
      sortProductsByFavorites()
    } else {
      location.reload() // Reload to restore original order
    }
    return false
  })
}

$(document).ready(function () {
  console.log('own scripts ready')
  var lines = linesOnPage('.product_data')
  var lines_now = $('.product_data').length / 2
  var add_products = (lines - lines_now) * 2
  var product_html = getProductHtml('product_data')
  _log('haluaisin lisata nain monta tuotetta viela ')
  _log(add_products)

  for (var i = 0; i < add_products; i++) {
    $('#content').append(product_html)
  }

  // Initialize favorites
  initializeFavorites()

  $('#language .btn').click(function () {
    console.log('klik')

    if ($(this).hasClass('fi')) {
      console.log('fi')
      $.ajax({
        type: 'GET',
        url: '/selosteet/setlanguage/fi',
        success: function (response) {
          $('#language .fi').addClass('active')
          $('#language .sv').removeClass('active')
          console.log('suomen kieli')
        },
      })
    }
    if ($(this).hasClass('sv')) {
      console.log('se')
      $.ajax({
        type: 'GET',
        url: '/selosteet/setlanguage/sv',
        success: function (response) {
          $('#language .sv').addClass('active')
          $('#language .fi').removeClass('active')
          console.log('suomen ja ruotsin kieli')
        },
      })
    }
    return false
  })
})
