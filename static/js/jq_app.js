$(document).ready( function () {

//Data tables
   $(".data-table").dataTable();

  // Acordion View Customar_Service


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
                     url: 'http://localhost:8000/panel/calendar/list/',
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


  //Funcion for Acordion Services Customer

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


  $('#btnService').change(function(){
        if (this.checked) {
            $('#panelService').attr("style", "display : initial;");
            $('#panelLoad').attr("style", "display : none;");
        }
        else {
            $('#panelService').attr("style", "display : none;");
            $('#panelLoad').attr("style", "display : initial;");
        }
   });

   $('#btnLoad').change(function(){
        if (this.checked) {
            $('#panelService').attr("style", "display : none;");
            $('#panelLoad').attr("style", "display : initial;");

        }
        else {
            $('#panelService').attr("style", "display : initial;");
            $('#panelLoad').attr("style", "display : none;");
        }
   });

$("#addService").on("click", function(){
    var total_item = parseInt($("#quantity").val()) * parseInt($('#item_unit').html()) || 0
   $('#tbItem > tbody:last-child').append('<tr><td style="display : none" id="item_id">'+$("#selecItem").val()+'</td><td id="item_quant">'+$("#quantity").val()+'</td><td id="item_name">'+$("#selecItem").val()+'</td><td id="item_unit">'+$("#selecItem").val()+'</td><td id="item_total" class="item_total" >'+parseInt($("#quantity").val()) * parseInt($("#selecItem").val())+'</td><td> <toolbar class="md-accent"><button data-type="info" data-trigger="focus" title="Add new Item" data-animation="am-flip-x" type="button" class="btn btn-danger test-tooltip"><i class="fa fa-times" aria-hidden="true"></i><tooltip md-direction="left"></tooltip></button></toolbar></td></tr>');
   var subtotal = 0;
   var total = 0;
   $(".item_total").each(function(){
	   subtotal =subtotal + parseInt($(this).html()) || 0;
    });
    $('#servSutotal').val(subtotal);

     total = subtotal - parseInt($('#discount').val() || 0)
    alert('Subtotal: '+subtotal+' Total: '+total)
});

$(".zoom-mouse").mouseenter(function(evento){
   $(this).animate({borderSpacing: "2px"}, "fast");
});

  $(".zoom-mouse").mouseleave(function(evento){
   $(this).animate({borderSpacing: "1px"},"fast");
});
 });
