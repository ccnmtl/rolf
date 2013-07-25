define([
    'jquery',
    'backbone',
    'models/log',
], function ($, Backbone) {

    var Result = Backbone.Model.extend({
        logs: [],
        status: "inprogress",

        stageElement: function() {
            return $("#stage-" + this.get('stage_id'));
        },

        status: function() {
            return this.get('status');
        },

        handleResults: function (result, runStageCallback) {
            this.set({
                logs: result.logs,
                status: result.status,
                stage_id: result.stage_id,
                end_time: result.end_time
            });
            this.continueOrCleanUp(runStageCallback);
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
