/**
 * Created by cody on 29/05/14.
 */

var Task = {};

Task.validate = function () {
    $("#task-form").validate({
        onfocusout: true,
        errorClass: "has-error",
        rules: {
            name: {
                required: true
            }
        }
    });
};