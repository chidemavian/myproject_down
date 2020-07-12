/**
 * Created by PyCharm.

 * Date: 3/12/12
 * Time: 11:30 AM
 * To change this template use File | Settings | File Templates.
 */
/*******************************************/
/*           edit reg                     */
/*****************************************/

function populateForm(pk){
    var url = "";

    if (window.location.pathname == "/student/edit/"){
        url = "/student/getform/?pk=" + pk;
    }
    else if (window.location.pathname == '/student/return/'){
        url = "/student/getform/return/?pk=" + pk;
    }
    else if (window.location.pathname == '/student/withdraw/'){
        url = "/student/getform/withdraw/?pk=" + pk;
    };

    if (url != ""){
        $.ajax({
            type: "GET",
            url: url,
            success: function(html){
                $("#regform").html(html)
            }
        });
    };
}

function getLGAs(){
    var state = $("#id_state_of_origin").val();
    var url = "/student/getlga/" + state + "/";
    $("#id_lga").val('');
    $("#id_lga").html('');
    if (state != undefined){
        $.ajax({
            type: "GET",
            url: url,
            success: function(data){
                var options = '';
                for (i=0; i<data.length; i++){
                    options += '<option value="' + data[i] +'">' + data[i] + '</option>'
                }
                $("#id_lga").append(options);
            }
        })
    }
}

function autocompleteStudentName(){
    var location = window.location.pathname;

    if (location == "/student/edit/" || location == "/student/withdraw/"){

    }
    else if (location == "/student/register/"){
        // do nothing
    }
    else {
        $("input#id_studentname").autocomplete({
            source: "/student/find/gone/",
            select: function(event, ui){
                $("input#id_studentname").val(ui.item.label);
                populateForm(ui.item.value);
                return false;
            }
        });
    };
}

function setDateWidget(){
    var dateFields = ["input#id_birth_date", "input#id_date_withdrawn"];
    var options = {
        changeYear: true,
        yearRange: "-25:+0",
        dateFormat: "yy-mm-dd",
        appendText: "yy-mm-dd",
        showAnim: "clip"
    }

    for (index=0; index < dateFields.length; index++){
        $(dateFields[index]).datepicker(options)
    }
}

function validatePhoneNumbers(){
    var location = window.location.pathname;
    if (location == '/student/register/' | location == '/student/edit/'){
        var phone_validator = {required: true, number: true, phoneUS: true, maxlength: 15};
        var message = "Please enter a valid phone number!";
        $("#form1").validate({
            rules: {
                fathernumber: phone_validator,
                mothernumber: phone_validator,
                next_of_kin_number: phone_validator
            },
            messages: {
                fathernumber: message,
                mothernumber: message,
                next_of_kin_number: message
            }
        })
    }
}

$(document).ready(
    function(){
        //$("#id_state_of_origin").attr('onchange', "javascript: getLGAs()");
        $("#id_state_of_origin").change(
            function(){
                getLGAs();
            });
        autocompleteStudentName();
        setDateWidget();
        validatePhoneNumbers();
    }
)