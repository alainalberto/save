$(document).ready( function () {

//Data tables
   $(".table").dataTable();

  // Acordion View Customar_Service
   $( "#service_forms" ).accordion();


   // Script Datapicker Input
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
			events: [
				{
					title: 'Business Lunch',
					start: '2017-05-03T13:00:00',
					constraint: 'businessHours'
				},
				{
					title: 'Meeting',
					start: '2017-05-13T11:00:00',
					constraint: 'availableForMeeting', // defined below
					color: '#05662D'
				},
				{
					title: 'Conference',
					start: '2017-05-18',
					end: '2017-05-20'
				},
				{
					title: 'Party',
					start: '2017-05-29',
					allDay: true,
					color: '#8D1307'
				},

				// areas where "Meeting" must be dropped
				{
					id: 'availableForMeeting',
					start: '2017-05-11T10:00:00',
					end: '2017-05-11T16:00:00',
					rendering: 'background'
				},
				{
					id: 'availableForMeeting',
					start: '2017-05-13T10:00:00',
					end: '2017-05-13T16:00:00',
					rendering: 'background'
				},

				// red areas where no events can be dropped
				{
					start: '2017-05-24',
					end: '2017-05-28',
					overlap: false,
					rendering: 'background',
					color: '#8D1307'
				},
				{
					start: '2017-05-06',
					end: '2017-05-08',
					overlap: false,
					rendering: 'background',
					color: '#AEEEEC'
				}
			],

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
			events: [
				{
					title: 'Business Lunch',
					start: '2017-05-03T13:00:00',
					constraint: 'businessHours'
				},
				{
					title: 'Meeting',
					start: '2017-05-13T11:00:00',
					constraint: 'availableForMeeting', // defined below
					color: '#05662D'
				},
				{
					title: 'Conference',
					start: '2017-05-18',
					end: '2017-05-20'
				},
				{
					title: 'Party',
					start: '2017-05-29',
					allDay: true,
					color: '#8D1307'
				},

				// areas where "Meeting" must be dropped
				{
					id: 'availableForMeeting',
					start: '2017-05-11T10:00:00',
					end: '2017-05-11T16:00:00',
					rendering: 'background'
				},
				{
					id: 'availableForMeeting',
					start: '2017-05-13T10:00:00',
					end: '2017-05-13T16:00:00',
					rendering: 'background'
				},

				// red areas where no events can be dropped
				{
					start: '2017-05-24',
					end: '2017-05-28',
					overlap: false,
					rendering: 'background',
					color: '#8D1307'
				},
				{
					start: '2017-05-06',
					end: '2017-05-08',
					overlap: false,
					rendering: 'background',
					color: '#AEEEEC'
				}
			],

		});




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