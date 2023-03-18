function loadResident(resident_id){
    selector = '#'+ resident_id + " div";
    if($.trim($(selector).html())!=''){
        return;
    }
    $.ajax({
        dataType: "html",
        url: '/admin/residents/' + resident_id,
        type: 'POST',
        success: function(result){
            $(selector).html(result);
        }
    });
}

function resident_type_event() {
    var value = $('#Resident\\ Type').val();
    if (value != "student") {
        console.log("student");
        console.log($("#branch_details #branch"));
        $("#branch_details #branch").attr('disabled', true);
        $("#branch_details #program").attr('disabled', true);
    }
    else{
        $("#branch_details #branch").attr('disabled', false);
        $("#branch_details #program").attr('disabled', false);
    }
}