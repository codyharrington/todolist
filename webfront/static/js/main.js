var Main = {};

Main.setActiveNav = function (navId) {
    $(".active").each(function () {
        $(this).removeClass("active");
    });
    var nav = $("#" + navId);
    nav.addClass("active");
};

