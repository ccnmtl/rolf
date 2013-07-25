define([
    'jquery'
], function ($) {
    var togglePre = function(el) {
        var pre = $($(el).parent().children("pre")[0]);
        if ($(el).hasClass("rolf-hidden")) {
            pre.show();
        } else {
            pre.hide();
        }
        $(el).toggleClass("rolf-hidden");
        $(el).toggleClass("rolf-showing");
    };

    var hideContent = function (td) {
        var h3 = $(td).children("h3")[0];
        $(td).children("pre").hide();
        $(h3).addClass("rolf-hidden");
        $(h3).click(function () {togglePre(h3); return false; });
    };
    return hideContent;
});
