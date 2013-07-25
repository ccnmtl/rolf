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
    'models/pushstatus', 'models/log', 'models/result',
    // utils
    'utils/hidecontent',
    // views
    'views/pushstatus', 'views/result'
], function ($, _, Backbone, // common
             PushStatus, Log, Result, // models
             hideContent, // utils
             PushStatusView, ResultView // views
            ) {
    var runAll = false;
    var stageIds = [];

    var push_status = new PushStatus();
    var psv = new PushStatusView({model: push_status});
    
    function runAllStages() {
        runAll = true;
        runStage(stageIds[0]);
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
        var r = new Result({push_status: push_status,
                            run_all: runAll,
                            stage_ids: stageIds
                           });

        var rv = new ResultView({model: r});

        stages.run(
            {
                'stage_id': stage_id,
                'rollback_id': rollback_id,
                'success': function (result) {
                    r.handleResults(result, runStage);
                },
                'error': myErrback
            });
        var stage_row = $("#stage-" + stage_id);
        stage_row.toggleClass("unknown");
        stage_row.toggleClass("inprogress");
    };
    
    function runStage(stage_id) {
        var stages = new Stages();
        new RunStageView({stages: stages, stage_id: stage_id});
    }

    function myErrback(result) {
        alert("stage failed: " + result);
    }

    function initPush() {
        $("td.stdout").each(function () { hideContent(this); });
        $("td.stderr").each(function () { hideContent(this); });
        $("td.command").each(function () { hideContent(this); });
        
        $("tr.stage-row").each(function () {
            var stage_id = $(this).attr('id').split("-")[1];
            stageIds.push(stage_id);
        });
        
        var autorun = $('#autorun');
        if (autorun.val() === 'autorun') {
            runAllStages();
        }
    }
    
    var NewMainView = function (options) {
        initPush();
    };
    
    $(document).ready(function () {
        new NewMainView();
    });
});
