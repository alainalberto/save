$(document).ready( function () {

//Data tables
   $(".table").dataTable();

  // Acordion View Customar_Service
   $( "#service_forms" ).accordion();

   $('.form_date').datetimepicker({
        language:  'ee',
        weekStart: 1,
        todayBtn:  1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		minView: 2,
		forceParse: 0
    });

   $( "#newCompany" ).visible = false;

    // run the currently selected effect
    function runEffect() {
      // get effect type from
      var selectedCompany = $( "#btnCompany" ).on("check");

      // some effects have required parameters
      if ( selectedCompany ) {
        $( "#newCompany" ).visible = true;
      }

      // Run the effect

    };

    //callback function to bring a hidden box back
    function callback() {
      setTimeout(function() {
        $( "#effect:visible" ).removeAttr( "style" ).fadeOut();
      }, 1000 );
    };

    // Set effect from select menu value
    $( "#button" ).on( "click", function() {
      runEffect();
    });
 });