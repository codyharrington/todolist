/**
 * Created by cody on 29/05/14.
 */

$(function () {
    $(".date-control").each(function () {
        $(this).datepicker();
    });

    $(".display-empty").each(function () {
        var empty_message = $("<div>", { class: "empty-message" }).html("No tasks found.");
        if ($(this).children().length === 0) {
            $(this).append(empty_message);
        } else {
            $(this).find(".empty-message").each(function () {
                $(this).remove();
            });
        }
    });

});