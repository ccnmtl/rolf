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

        stageElement: function() {
            return $("#stage-" + this.get('stage_id'));
        },

        status: function() {
            return this.get('status');
        },

        insertLogRows: function () {
            var stage_row = this.stageElement();
            var rows = this.makeLogRows();
            for (var i2 = rows.length - 1; i2 > -1; i2--) {
                stage_row.after($(rows[i2]));
            }
        },

        // are we done or might there be more stages to run?
        continuePush: function () {
            return this.get('run_all') && (this.status() !== "failed");
        },

        setPushStatus: function() {
            this.get('push_status')
                .set({status: this.status()});
        },

        noMoreStages: function () {
            return this.getNextStageId() === -1;
        },

        nextStageOrFinish: function (runStageCallback) {
            if (this.noMoreStages()) {
                this.setPushStatus();
                return;
            }
            runStageCallback(this.getNextStageId());
        },

        getNextStageId: function () {
            var current = this.get('stage_id');
            var stageIds = this.get('stage_ids');
            if (stageIds.length < 2) {
                return -1;
            }
            for (var i = 0; i < stageIds.length - 1; i++) {
                if (stageIds[i] == current) {
                    return stageIds[i + 1];
                }
            }
            // reached the end without hitting it
            return -1;
        },

        continueOrCleanUp: function (runStage) {
            if (this.continuePush()) {
                this.nextStageOrFinish(runStage);
            }
            if (this.status() === "failed") {
                this.setPushStatus();
                return;
            } 
            if (!this.get('run_all')) {
                if (this.noMoreStages()) {
                    // last stage
                    this.setPushStatus();
                    $('#runall-button').attr("disabled", "disabled");
                }
            }
        }
    });
    return Result;
});
