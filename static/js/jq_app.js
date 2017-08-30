$(document).ready( function () {
// Upper input text
   $('.upper').keyup(function() {
      $(this).val($(this).val().toUpperCase());
   });

//Data tables
   $(".data-table").DataTable();

// Messager
     $( ".messager" ).show(500, callback );
     function callback() {
      setTimeout(function() {
        $( ".messager:visible" ).removeAttr( "style" ).fadeOut();
      }, 1000 );
    };


// Script Datapicker Input
   $('.form_date').datetimepicker({
      language:  'en',
        weekStart: 1,
        todayBtn:  1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		minView: 2,
		forceParse: 0
   });


   $('.form_time').datetimepicker({
        language:  'en',
        weekStart: 1,
        todayBtn:  1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 1,
		minView: 0,
		maxView: 1,
		forceParse: 0
    });

// Efect View Panel
   $(".zoom-mouse").mouseenter(function(evento){
       $(this).animate({borderSpacing: "2px"}, "fast");
    });

   $(".zoom-mouse").mouseleave(function(evento){
      $(this).animate({borderSpacing: "1px"},"fast");
   });

// Script Calendar
    $('#calendar').fullCalendar({
			header: {
				left: 'prev,next today',
				center: 'title',
				right: 'month,agendaWeek,agendaDay,listMonth'
			},

			defaultDate: new Date(),
			navLinks: true, // can click day/week names to navigate views
			businessHours: true, // display business hours
			editable: true,
			events: {
                     url: '/panel/calendar/list/',
                     data: function() { // a function that returns an object
                            return {
                            dynamic_value: Math.random()
                            };
                     }
            }

	});


    $('#calendar_panel').fullCalendar({
			header: {
				left: 'prev,next',
				center: 'title',
				right: ''
			},
			defaultView: 'agendaDay',
			defaultDate: new Date(),
			navLinks: true, // can click day/week names to navigate views
			businessHours: true, // display business hours
			editable: true,
			events: {
                     url: 'http://localhost:8000/panel/calendar/list/',
                     data: function() { // a function that returns an object
                            return {
                            dynamic_value: Math.random()
                            };
                     }
            }

		});




 });



