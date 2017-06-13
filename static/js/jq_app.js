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


   $('.form_time').datetimepicker({
        language:  'fr',
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

   $(".btn_add").on("click", function() {
      var column1 = $(this).closest('tr').children()[0].textContent;
      var column2 = $(this).closest('tr').children()[1].textContent;
      var column3 = $(this).closest('tr').children()[2].textContent;
      var column4 = $(this).closest('tr').children()[3].textContent;
       if($("tbItem .copy_"+column1).length == 0) {
       $("#tbItem").append('<tr class="copy_'+column1+'"><td style="display : none">' + column1 + '</td><td class="col-md-1"><input type="number" class="entrada form-control" min="0" value="0"></td><td class="col-md-6">' + column2 + '</td><td class="col-md-6">' + column3 + '</td><td class="col-md-2">' + column4 + '</td><td class="subtotal col-md-2">0</td><td class="col-md-1"><toolbar class="md-accent"><a type="button" class="btn btn-danger btn_remove" data-type="info" data-trigger="focus" title="Add new Item" data-animation="am-flip-x" onclick="deleteitem(this.parentNode.parentNode.rowIndex)"><i class="fa fa-times-circle" aria-hidden="true"></i><tooltip md-direction="left"></tooltip></a></toolbar></td>');
       }

    });

   $("#btn_add_new").on("click", function() {
      var column1 = $('item').val();
      var column2 = $('account').val();
      var column3 = $('value').val();
      alert(column1, column2, column3);
       $("#tbItem").append('<tr class="copy_'+column1+'"><td style="display : none">' + column1 + '</td><td class="col-md-1"><input type="number" class="entrada form-control" min="0" value="0"></td><td class="col-md-6">' + column1 + '</td><td class="col-md-6">' + column2 + '</td><td class="col-md-2">' + column3 + '</td><td class="subtotal col-md-2">0</td><td class="col-md-1"><toolbar class="md-accent"><a type="button" class="btn btn-danger btn_remove" data-type="info" data-trigger="focus" title="Add new Item" data-animation="am-flip-x" onclick="deleteitem(this.parentNode.parentNode.rowIndex)"><i class="fa fa-times-circle" aria-hidden="true"></i><tooltip md-direction="left"></tooltip></a></toolbar></td>');
     });

    $("#tbItem").on("input", "input", function() {
       var input = $(this);
       var columns = input.closest("tr").children();
       var price = columns.eq(3).text();
       var calculated = input.val() * price;
       columns.eq(4).text(calculated.toFixed(2));
       sumar_columnas();

    });
    $(".btn_remove").click(function() {
          $('.btn_remove').parent().parent().remove();
    });

    function sumar_columnas(){
     var sum=0;
     var disc=0;
     if($('.discount').val() != 0){
       var disc = parseFloat($('.discount').val());
       }
    //itera cada input de clase .subtotal y la suma
    $('.subtotal').each(function() {
         sum += parseFloat($(this).text());
    });
    //cambia valor del total y lo redondea a la segunda decimal
    $('.servSutotal').val(sum.toFixed(2));
    var subtotal = sum.toFixed(2);
    var total = subtotal - disc
    $('.serviTotal').val(total.toFixed(2));
    }

    $('.discount').click(function(){
     if($('.discount').val() != 0){
       var disc = parseFloat($('.discount').val());
       var subtotal = parseFloat($('.servSutotal').val());
       var total = subtotal - disc
       $('.serviTotal').val(total.toFixed(2));
       }
    });


 });
  function deleteitem(i){
      document.getElementsByTagName("table")[0].setAttribute("id","tableid");
      document.getElementById("tableid").deleteRow(i);
    }
