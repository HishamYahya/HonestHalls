(function() {
	"use strict";

$(function () {
	$('[data-toggle="popover"]').popover()
	$('[data-toggle="tooltip"]').tooltip();
}

function setPopover() {

    $('.pop').on('mouseenter', function (e) {
        $('.pop').not(this).popover('destroy');
       if (!$(this).data("bs.popover")) {

            $(this).popover({
                placement: 'right',
                trigger: 'manual',
                html: true,
                title: InstName,
            });

        }

        $(this).popover('show');
    });
}


function showAlert(){
  if($("#myAlert").find("div#myAlert2").length==0){
    $("#myAlert").append("<div class='alert alert-success alert-dismissable' id='myAlert2'> <button type='button' class='close' data-dismiss='alert'  aria-hidden='true'>&times;</button> Success! message sent successfully.</div>");
  }
  $("#myAlert").css("display", "");
}



}

)



