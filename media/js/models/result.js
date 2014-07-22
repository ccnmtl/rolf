define([
    'jquery',
    'backbone',
    'models/log',
], function ($, Backbone) {

    var Result = Backbone.Model.extend({
        logs: [],
        status: 'inprogress',

        stageElement: function () {
            return $('#stage-' + this.get('stageId'));
        },

        getStatus: function () {
            return this.get('status');
        },

        handleResults: function (result, runStageCallback) {
            this.set({
                logs: result.logs,
                status: result.status,
                endTime: result.endTime
            });
            this.continueOrCleanUp(runStageCallback);
        },

        // are we done or might there be more stages to run?
        continuePush: function () {
            return this.get('runAll') && (this.getStatus() !== 'failed');
        },

        setPushStatus: function () {
            this.get('pushStatus')
                .set({status: this.getStatus()});
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
            var current = this.get('stageId');
            var stageIds = this.get('stageIds');
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
            if (this.getStatus() === 'failed') {
                this.setPushStatus();
                return;
            }
            if (!this.get('runAll')) {
                if (this.noMoreStages()) {
                    // last stage
                    this.setPushStatus();
                    $('#runall-button').attr('disabled', 'disabled');
                }
            }
        }
    });
    return Result;
});
