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
					constraint: 'businessHours',
					color: '#E74C3C'
				},
				{
					title: 'Meeting',
					start: '2017-05-13T11:00:00',
					constraint: 'availableForMeeting', // defined below
					color: '#27AE60'
				},
				{
					title: 'Conference',
					start: '2017-05-18',
					end: '2017-05-20',
					color: '#E74C3C'
				},
				{
					title: 'Party',
					start: '2017-05-29',
					allDay: true,
					color: '#DC7633'
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
					rendering: 'background',
					color: '#27AE60'
				},

				// red areas where no events can be dropped
				{
					start: '2017-05-24',
					end: '2017-05-28',
					overlap: false,
					color: '#27AE60'
				},
				{
					start: '2017-05-06',
					end: '2017-05-08',
					overlap: false,
					color: '#27AE60'
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

   $('#btnCompany').change(function(){
        if (this.checked) {
            $('#idcompany').attr("style", "display : initial;");
            $('#tabCompany').attr("style", "display : initial;");

        }
        else {
            $('#idcompany').attr("style", "display : none;");
            $('#tabCompany').attr("style", "display : none;");

        }
   });
   $('#btnPermit').change(function(){
        if (this.checked) {
            $('#tabPermit').attr("style", "display : initial;");
            $('#idpermit').attr("style", "display : initial;");
        }
        else {
            $('#tabPermit').attr("style", "display : none;");
            $('#idpermit').attr("style", "display : none;");
        }
   });
   $('#btnTitle').change(function(){
        if (this.checked) {
            $('#tabTitle').attr("style", "display : initial;");
            $('#idtitle').attr("style", "display : initial;");
        }
        else {
            $('#tabTitle').attr("style", "display : none;");
            $('#idtitle').attr("style", "display : none;");
        }
   });
   $('#btnPlate').change(function(){
        if (this.checked) {
            $('#tabPlate').attr("style", "display : initial;");
            $('#idplate').attr("style", "display : initial;");

        }
        else {
            $('#tabPlate').attr("style", "display : none;");
            $('#idplate').attr("style", "display : none;");
        }
   });
   $('#btnInsurence').change(function(){
        if (this.checked) {
            $('#tabInsurance').attr("style", "display : initial;");
            $('#idinsurance').attr("style", "display : initial;");
        }
        else {
            $('#tabInsurance').attr("style", "display : none;");
            $('#idinsurance').attr("style", "display : none;");
        }
   });
   $('#btnDot').change(function(){
        if (this.checked) {
            $('#tabDot').attr("style", "display : initial;");
            $('#iddot').attr("style", "display : initial;");
        }
        else {
            $('#tabDot').attr("style", "display : none;");
            $('#iddot').attr("style", "display : none;");
        }
   });
   $('#btnIfta').change(function(){
        if (this.checked) {
            $('#tabIfta').attr("style", "display : initial;");
            $('#idifta').attr("style", "display : initial;");
        }
        else {
            $('#tabIfta').attr("style", "display : none;");
            $('#idifta').attr("style", "display : none;");
        }
   });
 });

/*function showContent() {
        element = document.getElementById("#tabCompany");
        check = document.getElementById("#btnCompany");
        if (check.checked) {
            element.style.display='block';
        }
        else {
            element.style.display='none';
        }
    };*/