define([
    'jquery',
    'underscore',
    'backbone',

    'models/log',
    'views/logcommand',
    'views/logstdout',
    'views/logstderr'
], function ($, _, Backbone, Log, LogCommandView, LogStdoutView, LogStderrView) {
    var ResultView = Backbone.View.extend({
        initialize: function () {
            this.model.bind('change', this.render, this);
        },

        render: function () {
            this.insertLogRows();
            this.setStageClass();
            this.displayExecuteTime();
            return this;
        },

        markInProgress: function () {
            var stage_row = this.model.stageElement();
            stage_row.toggleClass("unknown");
            stage_row.toggleClass("inprogress");
        },

        displayExecuteTime: function () {
            $("#execute-" + this.model.get('stage_id'))
                .replaceWith($("<span/>", {'text': this.model.get('end_time') }));
        },

        setStageClass: function () {
            this.model.stageElement()
                .removeClass("inprogress")
                .removeClass("unknown")
                .addClass(this.model.status());
        },

        makeLogRows: function () {
            var rows = [];
            var logs = this.model.get('logs');
            for (var i = 0; i < logs.length; i++) {
                var log = logs[i];
                var l = new Log({log: log, result: this.model});
                if (log.command) {
                    var lvc = new LogCommandView({model: l});
                    rows.push(lvc.render().$el);
                }
                if (log.stdout) {
                    var lvo = new LogStdoutView({model: l});
                    rows.push(lvo.render().$el);
                }
                if (log.stderr) {
                    var lve = new LogStderrView({model: l});
                    rows.push(lve.render().$el);
                }
            }
            return rows;
        },

        insertLogRows: function () {
            var stage_row = this.model.stageElement();
            var rows = this.makeLogRows();
            for (var i2 = rows.length - 1; i2 > -1; i2--) {
                stage_row.after($(rows[i2]));
            }
        }
    });
    return ResultView;
});
