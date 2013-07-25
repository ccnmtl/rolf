define([
    'jquery', 'underscore', 'backbone',
    // models
    'models/pushstatus', 'models/result',
    // utils
    'utils/hidecontent',
    // views
    'views/pushstatus', 'views/result'
], function ($, _, Backbone,
             PushStatus, Result, // models
             hideContent, // utils
             PushStatusView, ResultView // views
) {
    var AppView = Backbone.View.extend({
        initialize: function () {
            this.push_status = new PushStatus();
            var psv = new PushStatusView({model: this.push_status});
    
            this.hideOutput();
        
            if ($('#autorun').val() === 'autorun') {
                this.runAll = true;
                this.runStage(this.getStageIds()[0]);
            }
        },

        hideOutput: function () {
            $("td.stdout").each(function () { hideContent(this); });
            $("td.stderr").each(function () { hideContent(this); });
            $("td.command").each(function () { hideContent(this); });
        },

        getStageResult:  function (options) {
            var url = "stage/?stage_id=" + options.stage_id +
                "&rollback_id=" + options.rollback_id;
            $.ajax({
                url: url,
                success: options.success,
                error: options.error
            });
        },

        runStage: function (stage_id) {
            var rollback_id = "";
            if ($('#rollback')) {
                rollback_id = $('#rollback').val() || "";
            }
            var r = new Result({
                stage_id: stage_id,
                push_status: this.push_status,
                run_all: this.runAll,
                stage_ids: this.getStageIds()
            });

            var rv = new ResultView({model: r});
            rv.markInProgress();
            var self = this;
            var callback = function (si) {
                self.runStage(si);
            };
            this.getStageResult({
                'stage_id': stage_id,
                'rollback_id': rollback_id,
                'success': function (result) {
                    r.handleResults(result, callback);
                },
                'error': this.myErrback
            });
        },

        myErrback: function (result) {
            alert("stage failed: " + result);
        },

        getStageIds: function () {
            var ids = [];
            $("tr.stage-row").each(function () {
                var stage_id = $(this).attr('id').split("-")[1];
                ids.push(stage_id);
            });
            return ids;
        }
    });
    return AppView;
});
