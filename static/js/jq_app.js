$(document).ready( function () {

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


  //Funcion for Acordion Services Customer

   /*$('#btnCompany').change(function(){
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
   });*/

// Insurance

$('#btnliability').change(function(){
        if (this.checked) {
            $('#liability').attr("style", "display : initial;");
        }
        else {
            $('#liability').attr("style", "display : none;");
        }
   });
$('#btncargo').change(function(){
        if (this.checked) {
            $('#cargo').attr("style", "display : initial;");
        }
        else {
            $('#cargo').attr("style", "display : none;");
        }
   });
$('#btnphysical').change(function(){
        if (this.checked) {
            $('#physical').attr("style", "display : initial;");
        }
        else {
            $('#physical').attr("style", "display : none;");
        }
   });


//Invoices
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

   $(".btn_add").click(function() {
      var column1 = $(this).closest('tr').children()[0].textContent;
      var column2 = $(this).closest('tr').children()[1].textContent;
      var column3 = $(this).closest('tr').children()[2].textContent;
      var column4 = $(this).closest('tr').children()[3].textContent;
      $('#tbItem tr').each(function(index, element){
          if($(element).find(".descript").val() == "" ){
            $(element).find(".precie").val(column4);
            $(element).find(".account").val(column1);
            $(element).find(".descript").val(column2);
             return false;
          }

       });

    });

    $(".btn_add_load").click(function() {
      var column1 = $(this).closest('tr').children()[0].textContent;
      var column2 = $(this).closest('tr').children()[1].textContent;
      var column3 = $(this).closest('tr').children()[2].textContent;
      var column4 = $(this).closest('tr').children()[3].textContent;
      var column5 = $(this).closest('tr').children()[4].textContent;
      var column7 = $(this).closest('tr').children()[6].textContent;
      $('#tbLoad tr').each(function(index, element){
          if($(element).eq(1).text() == "" ){
            $(element).eq(1).text() = column1;
            $(element).eq(2).text() = column2;
            $(element).eq(3).text() = column3;
            $(element).eq(4).text() = column4;
            $(element).eq(5).text() = column5;
            $(element).find(".load_id").val(column7);
             return false;
          }

       });

    });


   $(".listitem").on("change", function() {
      $('#valueunt').val();
      });


    $("#tbItem").on("input", "input", function() {
       var input = $(this).parents("tr").find('.entrada').val();
       var price = $(this).parents("tr").find('.precie').val();
       var porc = $(this).parents("tr").find('.tax').val();
       var total = input * price
       var tax = (total*porc)/100
       var calculated = total+tax;
       $(this).parents("tr").find('.subtotal').val(calculated.toFixed(2));
       sumar_columnas();
    });
    $(".btn_remove").click(function() {
        $(this).parents("tr").find('.entrada').val("");
        $(this).parents("tr").find('.precie').val("");
        $(this).parents("tr").find('.tax').val("");
        $(this).parents("tr").find('.descript').val("");
        $(this).parents("tr").find('.account').val('');
        $(this).parents("tr").find('.subtotal').val("")
        sumar_columnas();
    });

    function sumar_columnas(){
     var sum=0;
     var disc=0;
     if($('.discount').val() != 0){
       var disc = parseFloat($('.discount').val());
       }
    //itera cada input de clase .subtotal y la suma
    $('.subtotal').each(function() {
          v = 0;
          v = $(this).val();
         if (v != 0){
           sum += parseFloat(v);
           }
    });
    //cambia valor del total y lo redondea a la segunda decimal
    $('.servSutotal').val(sum.toFixed(2));
    var subtotal = sum.toFixed(2);
    var total = subtotal - disc
    $('.serviTotal').val(total.toFixed(2));
    }

    $('.discount').keyup(function(){
     if($('.discount').val() != 0){
       var disc = parseFloat($('.discount').val());
       var subtotal = parseFloat($('.servSutotal').val());
       var total = subtotal - disc
       $('.serviTotal').val(total.toFixed(2));
       }
    });

   //Search Customer
   $(".btn_add_cut").click(function() {
      var column = $(this).closest('tr').children()[5].textContent;
      $('#id_customers').val(column)
      $('#customerList').modal('hide');
    });


 });

  // Modal Save botton


