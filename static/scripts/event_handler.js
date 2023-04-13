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
            form_handler();
        }
    });
}
function loadHouseKeeping(housekeeper_id){
    selector = '#'+ housekeeper_id + " div";
    if($.trim($(selector).html())!=''){
        return;
    }
    $.ajax({
        dataType: "html",
        url: '/admin/housekeeping/' + housekeeper_id,
        type: 'POST',
        success: function(result){
            $(selector).html(result);
            form_handler();
        }
    });
}

function loadSecurity(security_id){
    selector = '#'+ security_id + " div";
    if($.trim($(selector).html())!=''){
        return;
    }
    $.ajax({
        dataType: "html",
        url: '/admin/security/' + security_id,
        type: 'POST',
        success: function(result){
            $(selector).html(result);
            form_handler();
        }
    });
}

function loadHostel(hostel_name){
    selector = '#'+ hostel_name + " div";
    if($.trim($(selector).html())!=''){
        return;
    }
    $.ajax({
        dataType: "html",
        url: '/admin/hostel/' + hostel_name,
        type: 'POST',
        success: function(result){
            $(selector).html(result);
            form_handler();
        }
    });
}

function loadFurniture(furniture_id){
    selector = '#'+ furniture_id + " div";
    if($.trim($(selector).html())!=''){
        return;
    }
    $.ajax({
        dataType: "html",
        url: '/admin/furniture/' + furniture_id,
        type: 'POST',
        success: function(result){
            $(selector).html(result);
            form_handler();
        }
    });
}
function loadRoom(room_no, hostel_name){
    selector = '#'+ hostel_name + '_' + room_no + " div";
    if($.trim($(selector).html())!=''){
        return;
    }
    $.ajax({
        dataType: "html",
        url: '/admin/rooms/' + hostel_name + '/' + room_no,
        type: 'POST',
        success: function(result){
            $(selector).html(result);
            form_handler();
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

// Handling form submissions
// Get the form element

function form_handler(){
    const form = document.getElementsByClassName('pop-up-form');
    console.log(form);
    Array.from(form).forEach(element => {
        // Add a submit event listener to the form
    element.addEventListener('submit', (e) => {
        // Prevent the default form submission behavior
        e.preventDefault();
    
        var url = element.action;
    
        // Create a new FormData object from the form data
        const formData = new FormData(element);
    
        // Send the form data through Ajax
        fetch(url, {
            method: 'POST',
            dataType: 'json',
            body: formData
        })
        .then(data => {
            if (data.ok){
                return data.json()
            }
            throw new Error('Something went wrong');
        })
        .then(data =>{
            // Handle the response data
            const messageModal = new bootstrap.Modal(document.getElementById("message-modal"));
            var toggle_off = "$('#message-modal').modal('hide');"
            $("#message-modal-body").html(data.message);
            if (data.reload){
                $("#message-modal-title").html("Success");
                $("#message-modal-close").attr("onclick", "location.reload()");
                $("#message-modal-ok").attr("onclick", "location.reload()");
            }
            else{
                $("#message-modal-title").html("Error");
                $("#message-modal-close").attr("onclick", toggle_off);
                $("#message-modal-ok").attr("onclick", toggle_off);
            }
            messageModal.toggle();
        })
        .catch(error => {
            // Handle errors
            const messageModal = new bootstrap.Modal(document.getElementById("message-modal"));
            $("#message-modal-body").html("Unexpected error occured. Please try again later.");
            $("#message-modal-close").attr("onclick", "");
            $("#message-modal-ok").attr("onclick", "");
        });
    });
});
}

form_handler();
