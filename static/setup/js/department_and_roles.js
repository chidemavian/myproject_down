/**
 * Created by PyCharm.
 * User: yusuf
 * Date: 3/8/12
 * Time: 12:05 PM
 * To change this template use File | Settings | File Templates.
 */

function renderAddDeptForm() {
    $.ajax({
        type:"GET",
        url:"/setup/departmentsandroles/add/",
        success:function (html) {
            $("#departmentform").html(html)
        }
    })
}

function renderRoleForm() {
    $.ajax({
        type:"GET",
        url:"/setup/departmentsandroles/add/role/",
        success:function (html) {
            $("#roleform").html(html)
        }
    })
}

function getDeptList() {
    $.ajax({
        type:"GET",
        url:"/setup/departmentsandroles/list/?page=1",
        success:function (html) {
            $("#departmentlist").html(html)
        }
    })
}

function getRoleList() {
    $.ajax({
        type:"GET",
        url:"/setup/departmentsandroles/list/role/?page=1",
        success:function (html) {
            $("#rolelist").html(html)
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

function addDepartment() {
    processForm("#department-form");
    window.location.reload();
}

function addRole() {
    processForm("#role-form");
    window.location.reload();
}

function deleteDepartment(pk) {
    $.ajax({
        type:"POST",
        url:"/setup/departmentsandroles/delete/" + pk + "/",
        success:getDeptList(),
        error:getDeptList()
    });
}

function deleteRole(pk) {
    $.ajax({
        type:"POST",
        url:"/setup/departmentsandroles/delete/role/" + pk + "/",
        success:getRoleList(),
        error:getRoleList()
    });
}

$(document).ready(function () {
    renderAddDeptForm();
    renderRoleForm();
    getDeptList();
    getRoleList();
})