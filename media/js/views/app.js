define([
    'jquery', 'underscore', 'backbone',
    // models
    'models/pushstatus', 'models/result',
    // utils
    'utils/hidecontent',
    // views
    'views/pushstatus', 'views/result'
], function($, _, Backbone,
             PushStatus, Result, // models
             hideContent, // utils
             PushStatusView, ResultView // views
) {
    var AppView = Backbone.View.extend({
        initialize: function() {
            this.pushStatus = new PushStatus();
            var psv = new PushStatusView({model: this.pushStatus});

            this.hideOutput();

            if ($('#autorun').val() === 'autorun') {
                this.runAll = true;
                this.runStage(this.getStageIds()[0]);
            }
        },

        hideOutput: function() {
            $('td.stdout').each(function() { hideContent(this); });
            $('td.stderr').each(function() { hideContent(this); });
            $('td.command').each(function() { hideContent(this); });
        },

        getStageResult:  function(options) {
            var url = 'stage/?stage_id=' + options.stageId +
                '&rollback_id=' + options.rollbackId;
            $.ajax({
                url: url,
                success: options.success,
                error: options.error
            });
        },

        runStage: function(stageId) {
            var rollbackId = '';
            if ($('#rollback')) {
                rollbackId = $('#rollback').val() || '';
            }
            var r = new Result({
                stageId: stageId,
                pushStatus: this.pushStatus,
                runAll: this.runAll,
                stageIds: this.getStageIds()
            });

            var rv = new ResultView({model: r});
            rv.markInProgress();
            var self = this;
            var callback = function(si) {
                self.runStage(si);
            };
            this.getStageResult({
                stageId: stageId,
                rollbackId: rollbackId,
                'success': function(result) {
                    r.handleResults(result, callback);
                },
                'error': this.myErrback
            });
        },

        myErrback: function(result) {
            alert('stage failed: ' + result);
        },

        getStageIds: function() {
            var ids = [];
            $('tr.stage-row').each(function() {
                var stageId = $(this).attr('id').split('-')[1];
                ids.push(stageId);
            });
            return ids;
        }
    });
    return AppView;
});
