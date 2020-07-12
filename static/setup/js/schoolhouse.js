/**
 * Created by PyCharm.
 * User: yusuf
 * Date: 3/8/12
 * Time: 12:06 PM
 * To change this template use File | Settings | File Templates.
 */

function getForm() {
    $.ajax({
        type:"GET",
        url:"/setup/schoolhouse/add/",
        success:function (html) {
            $("#houseform").html(html);
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

function addHouse() {
    processForm("#house-form");
    window.location.reload();
}

function deleteHouse(pk) {
    $.ajax({
        type:"POST",
        url:"/setup/schoolhouse/delete/" + pk + "/",
        success:getList(),
        error:getList()
    })
}

function getList() {
    $.ajax({
        type:"GET",
        url:"/setup/schoolhouse/list/?page=1",
        success:function (html) {
            $("#houselist").html(html);
        }
    })
}

$(document).ready(function () {
    getForm();
    getList();
})