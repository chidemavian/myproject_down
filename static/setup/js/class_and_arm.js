/**
 * Created by PyCharm.
 * User: yusuf
 * Date: 2/28/12
 * Time: 12:01 PM
 * To change this template use File | Settings | File Templates.
 */

function renderAddClassForm() {
    $.ajax({
        type:"GET",
        url:"/setup/class/add/",
        success:function (html) {
            $("#classform").html(html)
        }
    })
}

function renderArmForm() {
    $.ajax({
        type:"GET",
        url:"/setup/class/add/arm/",
        success:function (html) {
            $("#armform").html(html)
        }
    })
}

function getClassList() {
    $.ajax({
        type:"GET",
        url:"/setup/class/list/?page=1",
        success:function (html) {
            $("#classlist").html(html)
        }
    })
}

function getArmList() {
    $.ajax({
        type:"GET",
        url:"/setup/class/list/arm/?page=1",
        success:function (html) {
            $("#armlist").html(html)
        }
    })
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

function addClassItem() {
    processForm("#class-form");
    window.location.reload();
}

function addArm() {
    processForm("#arm-form");
    window.location.reload();
}

function deleteClassItem(pk) {
    $.ajax({
        type:"POST",
        url:"/setup/class/delete/" + pk + "/"
    });
    window.location.reload();
}

function deleteArm(pk) {
    $.ajax({
        type:"POST",
        url:"/setup/class/delete/arm/" + pk + "/"
    });
    window.location.reload();
}

$(document).ready(function () {
    renderAddClassForm();
    renderArmForm();
    getClassList();
    getArmList();
})