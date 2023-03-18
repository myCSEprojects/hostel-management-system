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