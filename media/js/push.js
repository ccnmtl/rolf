(function (jQuery) {
    var M = MochiKit;
    var MA = MochiKit.Async;
    var MB = MochiKit.Base;
    var MD = MochiKit.DOM;
    var $ = MochiKit.DOM.$;
    var runAll = false;
    var stageIds = [];

    function runAllStages() {
        runAll = true;
        runStage(stageIds[0]);
    }

    var Stages = function () {
    };
    Stages.prototype.run = function (options) {
        var d = MA.loadJSONDoc("stage/?" + MB.queryString({
            'stage_id' : options.stage_id,
            'rollback_id' : options.rollback_id
        }));
        d.addCallback(options.success);
        d.addErrback(options.error);
    };

    var RunStageView = function (options) {
        var stages = options.stages;
        var stage_id = options.stage_id;
        var rollback_id = "";
        if (jQuery('#rollback')) {
            rollback_id = jQuery('#rollback').val();
        }
        stages.run(
            {
                'stage_id': stage_id,
                'rollback_id': rollback_id,
                'success': stageResults,
                'error': myErrback
            });
        var stage_row = jQuery("#stage-" + stage_id);
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

    function makeLogTR(log, result) {
        var tr = jQuery("<tr>");
        var td = jQuery("<td>", {"colspan": "2", "class": "command"});
        var h3 = jQuery("<h3>", {"text": "Code"});
        var pre = jQuery("<pre>", {"text": log.command});
        td.append(h3).append(pre);
        if (result.status === "ok") {
            hideContent(td);
        }
        tr.append(td);
        return tr.get();
    }

    function makeStdoutTR(log, result) {
        var tr = jQuery("<tr>");
        var td = jQuery("<td>", {'colspan' : '2', 'class' : 'stdout'});
        var h3 = jQuery("<h3>", {"text": "STDOUT"});
        var pre = jQuery("<pre>", {"text": log.stdout});
        td.append(h3).append(pre);
        if (result.status === "ok") {
            hideContent(td);
        }
        tr.append(td);
        return tr.get();
    }

    function makeStderrTR(log, result) {
        var tr = jQuery("<tr>");
        var td = jQuery("<td>", {'colspan' : '2', 'class' : 'stderr'});
        var h3 = jQuery("<h3>", {"text": "STDERR"});
        var pre = jQuery("<pre>", {"text": log.stderr});
        td.append(h3).append(pre);
        if (result.status === "ok") {
            hideContent(td);
        }
        tr.append(td);
        return tr;
    }

    function setPushStatus(result) {
        jQuery("#push-status")
            .removeClass("inprogress")
            .addClass(result.status)
            .text(result.status);
    }

    function makeLogRows(result) {
        var rows = [];

        for (var i = 0; i < result.logs.length; i++) {
            var log = result.logs[i];
            if (log.command) {
                rows.push(makeLogTR(log, result));
            }
            if (log.stdout) {
                rows.push(makeStdoutTR(log, result));
            }
            if (log.stderr) {
                rows.push(makeStderrTR(log, result));
            }
        }
        return rows;
    }

    function insertLogRows(stage_row, rows) {
        for (var i2 = rows.length - 1; i2 > -1; i2--) {
            jQuery(stage_row).after(jQuery(rows[i2]));
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
            setPushStatus(result);
        }
    }

    function stageResults(result) {
        var stage_row = $("stage-" + result.stage_id);

        var rows = makeLogRows(result);
        insertLogRows(stage_row, rows);

        jQuery("#stage-" + result.stage_id)
            .removeClass("inprogress")
            .removeClass("unknown")
            .addClass(result.status);

        jQuery("#execute-" + result.stage_id)
            .replaceWith(jQuery("<span/>", {'text': result.end_time }));

        if (continuePush(result)) {
            nextStageOrFinish(result);
        }
        if (result.status === "failed") {
            setPushStatus(result);
        } else {
            if (!runAll) {
                if (getNextStageId(result.stage_id) === -1) {
                    // last stage
                    setPushStatus(result);
                    jQuery('#runall-button').attr("disabled", "disabled");
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

    function togglePre(el) {
        var pre = jQuery(jQuery(el).parent().children("pre")[0]);
        if (jQuery(el).hasClass("rolf-hidden")) {
            pre.show();
        } else {
            pre.hide();
        }
        jQuery(el).toggleClass("rolf-hidden");
        jQuery(el).toggleClass("rolf-showing");
    }

    function hideContent(td) {
        var h3 = jQuery(td).children("h3")[0];
        jQuery(td).children("pre").hide();
        jQuery(h3).addClass("rolf-hidden");
        jQuery(h3).click(function () {togglePre(h3); return false; });
    }

    function initPush() {
        jQuery("td.stdout").each(function () { hideContent(this); });
        jQuery("td.stderr").each(function () { hideContent(this); });
        jQuery("td.command").each(function () { hideContent(this); });

        jQuery("tr.stage-row").each(function () {
            var stage_id = jQuery(this).attr('id').split("-")[1];
            stageIds.push(stage_id);
        });

        var autorun = jQuery('#autorun');
        if (autorun.val() === 'autorun') {
            runAllStages();
        }
    }

    MD.addLoadEvent(initPush);
}(jQuery));
