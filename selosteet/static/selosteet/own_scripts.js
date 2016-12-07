$(document).ready(function() {
      console.log("readi");
  $("#about-btn").click( function(event) {
  alert("You clicked the button using JQuery!");
  });
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
