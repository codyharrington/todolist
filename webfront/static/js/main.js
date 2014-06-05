var Main = {};

Main.setActiveNav = function (navId) {
    $(".active").each(function () {
        $(this).removeClass("active");
    });
    var nav = $("#" + navId);
    nav.addClass("active");
};

Main.generateRecaptcha = function (recaptcha_pub_key, recaptcha_div_id, form_id) {
    Recaptcha.create(recaptcha_pub_key, recaptcha_div_id, { theme: "clean" });

    $("#" + form_id).submit(function(event) {
        var captcha_challenge = $("<input>", {type: "hidden", name: "c_challenge"}).val(Recaptcha.get_challenge());
        var captcha_response = $("<input>", {type: "hidden", name: "c_response"}).val(Recaptcha.get_response());
        $('#' + form_id).append(captcha_challenge).append(captcha_response);
        Recaptcha.destroy();
    });
};

