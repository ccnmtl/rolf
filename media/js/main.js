require.config({
    paths: {
        // Major libraries
        jquery: 'libs/jquery/jquery-1.7.2.min',
        underscore: 'libs/underscore/underscore-1.5.1-min',
        backbone: 'libs/backbone/backbone-1.0.0-min',

        // Require.js plugins
        text: 'libs/require/text',
        order: 'libs/require/order'
    },
    urlArgs: "bust=" +  (new Date()).getTime(),
    shim: {
        'backbone': {
            deps: ['jquery', 'underscore'],
            exports: 'Backbone'
        },
        'underscore': {
            exports: '_'
        }
    }
});

require([
    // common
    'jquery', 'underscore', 'backbone',
    // models
    'models/pushstatus', 'models/result',
    // utils
    'utils/hidecontent',
    // views
    'views/pushstatus', 'views/result'
], function ($, _, Backbone, // common
             PushStatus, Result, // models
             hideContent, // utils
             PushStatusView, ResultView // views
            ) {
    var runAll = false;

    var push_status = new PushStatus();
    var psv = new PushStatusView({model: push_status});
    
    function runAllStages() {
        runAll = true;
        runStage(getStageIds()[0]);
    }
    
    var Stages = function () {
    };
    Stages.prototype.run = function (options) {
        var url = "stage/?stage_id=" + options.stage_id +
            "&rollback_id=" + options.rollback_id;
        $.ajax({
            url: url,
            success: options.success,
            error: options.error
        });
    };
    
    var RunStageView = function (options) {
        var stages = options.stages;
        var stage_id = options.stage_id;
        var rollback_id = "";
        if ($('#rollback')) {
            rollback_id = $('#rollback').val() || "";
        }
        var r = new Result({
            stage_id: stage_id,
            push_status: push_status,
            run_all: runAll,
            stage_ids: getStageIds()
        });

        var rv = new ResultView({model: r});
        rv.markInProgress();

        stages.run(
            {
                'stage_id': stage_id,
                'rollback_id': rollback_id,
                'success': function (result) {
                    r.handleResults(result, runStage);
                },
                'error': myErrback
            });
    };
    
    function runStage(stage_id) {
        var stages = new Stages();
        new RunStageView({stages: stages, stage_id: stage_id});
    }

    function myErrback(result) {
        alert("stage failed: " + result);
    }

    function hideOutput() {
        $("td.stdout").each(function () { hideContent(this); });
        $("td.stderr").each(function () { hideContent(this); });
        $("td.command").each(function () { hideContent(this); });
    }

    function getStageIds() {
        var ids = [];
        $("tr.stage-row").each(function () {
            var stage_id = $(this).attr('id').split("-")[1];
            ids.push(stage_id);
        });
        return ids;
    }

    var NewMainView = function (options) {
        hideOutput();
        
        if ($('#autorun').val() === 'autorun') {
            runAllStages();
        }
    };
    
    $(document).ready(function () {
        new NewMainView();
    });
});
