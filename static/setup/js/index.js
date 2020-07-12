/**
 * Author: Abraham Yusuf <bb6xt@yahoo.com>
 * Date: 3/26/12
 * Time: 10:15 AM
 */

function renderForm(edit) {
    var url = '';
    if (edit == true){
        url = '/setup/school/edit/'
    }
    else{
        url = '/setup/school/'
    }
    $.ajax({
        type:"GET",
        url: url,
        success:function (html) {
            $("#schoolFormDialog").html(html)
        }
    })
}

function makeDialog(edit) {
    if (edit == true){
        var buttons = {
            'Update': function(){
                $("#schoolFormDialog").dialog("close");
                setupSchool("#school-form");
            },
            'Cancel': function () {
                $("#schoolFormDialog").dialog("close")
            }
        }
    }
    else{
        var buttons = {
            'Save': function(){
                $("#schoolFormDialog").dialog("close");
                setupSchool("#school-form");
            },
            'Cancel': function () {
                $("#schoolFormDialog").dialog("close")
            }
        }
    }
    var dialogOpts = {
        //autoOpen:false,
        title:'Setup School',
        modal:true,
        buttons: buttons
    };
    $("#schoolFormDialog").dialog(dialogOpts);
}

function setupSchool(form){
    $.ajax({
        type: "POST",
        url: $(form).attr("action"),
        data: $(form).serialize(),
        success: function(data){
            $("body").message(data);
        }
    })
}

function processAction(edit){
    renderForm(edit);
    makeDialog(edit);
    $("#schoolFormDialog").dialog("open");
}

/*
$(document).ready(
    function(){
        return false;
    }
)
*/