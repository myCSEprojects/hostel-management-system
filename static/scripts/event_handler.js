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
const form = document.getElementById('pop-up-form');

// Add a submit event listener to the form
form.addEventListener('submit', (e) => {
  // Prevent the default form submission behavior
  e.preventDefault();

  var url = form.action;

  // Create a new FormData object from the form data
  const formData = new FormData(form);

  // Send the form data through Ajax
  fetch(url, {
    method: 'POST',
    dataType: 'json',
    body: formData
  })
  .then(data => data.json())
  .then(data =>{
    // Handle the response data
    console.log(data);
    const messageModal = new bootstrap.Modal(document.getElementById("message-modal"));
    $("#message-modal-body").html(data.message);
    if (data.reload){
        $("#message-modal-close").attr("onclick", "location.reload()");
        $("#message-modal-ok").attr("onclick", "location.reload()");
    }
    else{
        $("#message-modal-close").attr("onclick", "");
        $("#message-modal-ok").attr("onclick", "");
    }
    messageModal.toggle();
  })
  .catch(error => {
    // Handle errors
  });
});
