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
    'jquery',
    'underscore',
    'backbone',
    'models/pushstatus',
    'models/log',
    'utils/hidecontent',
    'views/pushstatus',
    'views/logcommand',
    'views/logstderr',
    'views/logstdout'
], function ($, _, Backbone, PushStatus, Log, hideContent, PushStatusView, LogCommandView,
             LogStderrView, LogStdoutView) {
    var runAll = false;
    var stageIds = [];
    
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
        stages.run(
            {
                'stage_id': stage_id,
                'rollback_id': rollback_id,
                'success': stageResults,
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

    var push_status = new PushStatus();
    var psm = new PushStatusView({model: push_status});
    
    function makeLogRows(result) {
        var rows = [];
        
        for (var i = 0; i < result.logs.length; i++) {
            var log = result.logs[i];
            var l = new Log({log: log, result: result});
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
    }
    
    function insertLogRows(stage_row, rows) {
        for (var i2 = rows.length - 1; i2 > -1; i2--) {
            $(stage_row).after($(rows[i2]));
        }
    }
    
    // are we done or might there be more stages to run?
    function continuePush(result) {
        return runAll && (result.status !== "failed");
    }
    
    function nextStageOrFinish(result) {
        var nextId = getNextStageId(result.stage_id);
        if (nextId !== -1) {
            runStage(nextId);
        } else {
            push_status.set({status: result.status});
        }
    }
    
    function stageResults(result) {
        var stage_row = $("#stage-" + result.stage_id);
        
        var rows = makeLogRows(result);
        insertLogRows(stage_row, rows);
        
        $("#stage-" + result.stage_id)
            .removeClass("inprogress")
            .removeClass("unknown")
            .addClass(result.status);
        
        $("#execute-" + result.stage_id)
            .replaceWith($("<span/>", {'text': result.end_time }));
        
        if (continuePush(result)) {
            nextStageOrFinish(result);
        }
        if (result.status === "failed") {
            push_status.set({status: result.status});
        } else {
            if (!runAll) {
                if (getNextStageId(result.stage_id) === -1) {
                    // last stage
                    push_status.set({status: result.status});
                    $('#runall-button').attr("disabled", "disabled");
                }
            }
        }
    }
    
    function getNextStageId(current) {
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
