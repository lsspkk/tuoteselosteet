 /* calculate A4 proportions, and how many lines fit on to one page */
function linesOnPage(css_selector) {
   var width = $('#content').first().width();
   var a4Height = (width/210) * (297-30);
			 
   if( $(css_selector).length > 0 ) {
         return Math.floor(a4Height / $(css_selector).first().height());
   }
   return 1;
}

function _log(x) { console.log(x); }


function getProductHtml(css_selector) {
  var list = document.getElementsByClassName(css_selector);
  if( list.length > 0 )
    return list[0].outerHTML;
  return '';
}

$(document).ready(function() {
   console.log("own scripts ready");
   var lines = linesOnPage('.product_data');
   var lines_now = $('.product_data').length/2;
   var add_products = (lines-lines_now)*2;
   var product_html = getProductHtml('product_data');
   _log("haluaisin lisata nain monta tuotetta viela ");
   _log(add_products);
   
   
   for( var i=0; i < add_products; i++ ) {
     $('#content').append(product_html);
   }

   

  $("#language .btn").click(function() {
      console.log("klik");

        if( $(this).hasClass("fi") ) {
          console.log("fi");
          $.ajax({
              type: "GET",
              url: '/selosteet/setlanguage/fi',
              success: function(response){
                  $('#language .fi').addClass('active');
                  $('#language .sv').removeClass('active');
                  console.log("suomen kieli");
              }
          });
        }
        if( $(this).hasClass("sv") ) {
          console.log("se");
          $.ajax({
              type: "GET",
              url: '/selosteet/setlanguage/sv',
              success: function(response){
                $('#language .sv').addClass('active');
                $('#language .fi').removeClass('active');
                  console.log("suomen ja ruotsin kieli");
              }
          });
        }
        return false;
    });
});
