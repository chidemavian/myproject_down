/**
 * Created by PyCharm.
 *
 * Date: 3/2/12
 * Time: 10:36 AM
 * To change this template use File | Settings | File Templates.
 */

function setFormBody() {
    $.ajax({
        type:"GET",
        url:"/setup/subject/add/",
        success:function (html) {
            $("#subjectEditDialog").html(html);
        }
    })
}

function makeSubjectEditDialog() {
    var dialogOpts = {
        autoOpen:false,
        title:'Add Subject',
        modal:true,
        buttons:{
            'Add':function () {
                $("#subjectEditDialog").dialog("close");
                processForm("#subject-form");
            },
            'Cancel':function () {
                $("#subjectEditDialog").dialog("close")
            }
        }
    };
    $("#subjectEditDialog").dialog(dialogOpts);
}

function processForm(form) {
    var url = $(form).attr("action");
    $.ajax({
        type:"POST",
        url:url,
        data:$(form).serialize(),
        success:function (html) {
            $(form).parent().html(html)
        }
    })
}

function getSubjectList() {
    $.ajax({
        type:"POST",
        url:"/setup/subject/list/" + $("#id_rclass").val() + "/",
        success:function (html) {
            $("#swap-data-table").html(html);
        }
    })
}

function openSubjectEditDialog() {
    setFormBody();
    makeSubjectEditDialog();
    $("#subjectEditDialog").dialog("open");
}

function deleteItem(pk) {
    $.ajax({
        url:"/setup/subject/delete/" + pk + "/",
        type:"POST",
        success:getSubjectList(),
        error:getSubjectList()
    })
}
/*
 $(document).ready(
 function(){

 }
 );
 */