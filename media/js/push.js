(function () {
    var M = MochiKit;
    var MA = MochiKit.Async;
    var MB = MochiKit.Base;
    var MD = MochiKit.DOM;
    var MI = MochiKit.Iter;
    var MS = MochiKit.Style;
    var $ = MochiKit.DOM.$;
    var runAll = false;
    var stageIds = [];

    function runAllStages() {
        runAll = true;
        runStage(stageIds[0]);
    }

    function runStage(stage_id) {
        var rollback_id = "";
        if ($('rollback')) {
            rollback_id = $('rollback').value;
        }
        var d = MA.loadJSONDoc("stage/?" + MB.queryString({
            'stage_id' : stage_id,
            'rollback_id' : rollback_id
        }));
        d.addCallback(stageResults);
        d.addErrback(myErrback);
        var stage_row = $("stage-" + stage_id);
        MD.swapElementClass(stage_row, "unknown", "inprogress");
    }

    function myErrback(result) {
        alert("stage failed: " + result);
    }

    function makeLogTR(log, result) {
        var td = MD.TD({'colspan' : '2', 'class' : 'command'},
                       [MD.H3(null, "Code"),
                        MD.PRE(null, log.command)]);
        if (result.status === "ok") {
            hideContent(td);
        }
        return MD.TR({}, td);
    }

    function makeStdoutTR(log, result) {
        var stdouttd = MD.TD({'colspan' : '2', 'class' : 'stdout'},
                             [MD.H3(null, "STDOUT"), MD.PRE(null, log.stdout)]);
        if (result.status === "ok") {
            hideContent(stdouttd);
        }
        return MD.TR({}, stdouttd);
    }

    function makeStderrTR(log, result) {
        var stderrtd = MD.TD({'colspan' : '2', 'class' : 'stderr'},
                             [MD.H3(null, "STDERR"), MD.PRE(null, log.stderr)]);
        if (result.status === "ok") {
            hideContent(stderrtd);
        }
        return MD.TR({}, stderrtd);
    }

    function setPushStatus(result) {
        MD.swapDOM(
            $('push-status'),
            MD.DIV({'id' : 'push-status',
                    'class' : result.status}, result.status));
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

    function stageResults(result) {
        var stage_row = $("stage-" + result.stage_id);

        var rows = makeLogRows(result);

        for (var i2 = rows.length - 1; i2 > -1; i2--) {
            MD.insertSiblingNodesAfter(stage_row, rows[i2]);
        }

        MD.swapElementClass(stage_row, "inprogress", result.status);
        MD.swapElementClass(stage_row, "unknown", result.status);
        MD.swapDOM($("execute-" + result.stage_id), MD.SPAN(null, result.end_time));
        if (runAll && (result.status !== "failed")) {
            var nextId = getNextStageId(result.stage_id);
            if (nextId !== -1) {
                runStage(nextId);
            } else {
                setPushStatus(result);
            }
        }

        if (result.status === "failed") {
            setPushStatus(result);
        } else {
            if (!runAll) {
                if (getNextStageId(result.stage_id) === -1) {
                    // last stage
                    setPushStatus(result);
                    $('runall-button').disabled = true;
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
        var td = el.parentNode;
        var pre = td.getElementsByTagName("pre")[0];
        if (MD.hasElementClass(el, "rolf-hidden")) {
            MS.showElement(pre);
            MD.swapElementClass(el, "rolf-hidden", "rolf-showing");
        } else {
            MS.hideElement(pre);
            MD.swapElementClass(el, "rolf-showing", "rolf-hidden");
        }
    }

    function hideContent(td) {
        var h3 = td.getElementsByTagName("h3")[0];
        var pre = td.getElementsByTagName("pre")[0];
        MS.hideElement(pre);
        MD.addElementClass(h3, "rolf-hidden");
        h3.onclick = function () {togglePre(h3); return false; };
    }

    function initPush() {
        var contents = MD.getElementsByTagAndClassName("td", "stdout");
        for (var i = 0; i < contents.length; i++) {
            hideContent(contents[i]);
        }

        var errors = MD.getElementsByTagAndClassName("td", "stderr");
        for (var i2 = 0; i2 < errors.length; i2++) {
            hideContent(errors[i2]);
        }

        var commands = MD.getElementsByTagAndClassName("td", "command");
        for (var i3 = 0; i3 < commands.length; i3++) {
            hideContent(commands[i3]);
        }

        MI.forEach(MD.getElementsByTagAndClassName("tr", "stage-row"),
                function (element) {
                    var stage_id = element.id.split("-")[1];
                    stageIds.push(stage_id);
                }
               );

        var autorun = $('autorun');
        if (autorun) {
            if (autorun.value === 'autorun') {
                runAllStages();
            }
        }
    }

    MD.addLoadEvent(initPush);
}());
