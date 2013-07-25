define([
    'jquery',
    'backbone',
    'models/log',
    'views/logcommand',
    'views/logstdout',
    'views/logstderr'
], function ($, Backbone, Log, LogCommandView, LogStdoutView, LogStderrView) {

    var Result = Backbone.Model.extend({
        logs: [],
        status: "inprogress",
        makeLogRows: function () {
            var rows = [];
            var logs = this.get('logs');
            for (var i = 0; i < logs.length; i++) {
                var log = logs[i];
                var l = new Log({log: log, result: this});
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
        insertLogRows: function (stage_row) {
            var rows = this.makeLogRows();
            for (var i2 = rows.length - 1; i2 > -1; i2--) {
                $(stage_row).after($(rows[i2]));
            }
        }
    });
    return Result;
});
