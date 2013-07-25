define([
    'jquery',
    'underscore',
    'backbone'
], function ($, _, Backbone) {
    var ResultView = Backbone.View.extend({
        displayExecuteTime: function() {
            $("#execute-" + this.model.get('stage_id'))
                .replaceWith($("<span/>", {'text': this.model.get('end_time') }));
        },
        setStageClass: function () {
            this.model.stageElement()
                .removeClass("inprogress")
                .removeClass("unknown")
                .addClass(this.model.status());
        }
    });
    return ResultView;
});
