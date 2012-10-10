
var runAll = false;
var stageIds = new Array();

function runAllStages() {
   runAll = true;
   runStage(stageIds[0]);
}

function runStage(stage_id) {
   var rollback_id = "";
   if ($('rollback')) {
      rollback_id = $('rollback').value;
   }
   d = loadJSONDoc("stage/?" + queryString({
      'stage_id' : stage_id,
      'rollback_id' : rollback_id
   }));
   d.addCallback(stageResults);
   d.addErrback(myErrback);
   var stage_row = $("stage-" + stage_id);
   swapElementClass(stage_row,"unknown","inprogress");
}

function myErrback(result) {
  alert("stage failed: " + result);
}

function stageResults(result) {
   var stage_row = $("stage-" + result.stage_id);

   var rows = new Array();

   for (var i=0;i<result.logs.length;i++) {
      var log = result.logs[i];

      if (log.command) {
	 var td = TD({'colspan' : '2', 'class' : 'command'},
		     [H3(null,"Code"),
		     PRE(null,log.command)]);
	 if (result.status == "ok") {
	    hideContent(td);
	 }
	 rows.push(TR({},td));

      }

      if (log.stdout) {
	 var td = TD({'colspan' : '2','class' : 'stdout'},
		     [H3(null,"STDOUT"),PRE(null,log.stdout)]);
	 if (result.status == "ok") {
	    hideContent(td);
	 }
	 var stdout_row = TR({},td);
	 rows.push(stdout_row);
      }

      if (log.stderr) {
	 var td = TD({'colspan' : '2', 'class' : 'stderr'},
		     [H3(null,"STDERR"),PRE(null,log.stderr)]);
	 if (result.status == "ok") {
	    hideContent(td);
	 }
	 var stderr_row = TR({},td);
	 rows.push(stderr_row);
      }
   }

   for (var i=rows.length - 1;i > -1;i--) {
      insertSiblingNodesAfter(stage_row,rows[i]);
   }

   swapElementClass(stage_row,"inprogress",result.status);
   swapElementClass(stage_row,"unknown",result.status);
   swapDOM($("execute-" + result.stage_id),SPAN(null,result.end_time));
   if (runAll && (result.status != "failed")) {
      var nextId = getNextStageId(result.stage_id);
      if (nextId != -1) {
	 runStage(nextId);
      } else {
	 // last stage. here we can set the push's status
	 var newStatus = DIV({'id' : 'push-status',
	    'class' : result.status},result.status);
	 swapDOM($('push-status'),newStatus);
      }
   }

   if (result.status == "failed") {
      var newStatus = DIV({'id' : 'push-status',
	    'class' : result.status},result.status);
      swapDOM($('push-status'),newStatus);
   } else {
      if (!runAll) {
	 if (getNextStageId(result.stage_id) == -1) {
	    // last stage
	    var newStatus = DIV({'id' : 'push-status',
	    'class' : result.status},result.status);
	    swapDOM($('push-status'),newStatus);
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
	 return stageIds[i+1];
      }
   }
   // reached the end without hitting it
   return -1;
}

function togglePre (el) {
	var td = el.parentNode;
	var pre = td.getElementsByTagName("pre")[0];
	if (hasElementClass(el,"rolf-hidden")) {
		showElement(pre);
		swapElementClass(el,"rolf-hidden","rolf-showing");
	} else {
		hideElement(pre);
		swapElementClass(el,"rolf-showing","rolf-hidden");
	}
}

function hideContent (td) {
	var h3 = td.getElementsByTagName("h3")[0];
	var pre = td.getElementsByTagName("pre")[0];
	hideElement(pre);
	addElementClass(h3,"rolf-hidden");
	h3.onclick = function () {togglePre(h3);return false;}
}

function initPush () {
	var contents = getElementsByTagAndClassName("td","stdout");
	for (var i = 0; i < contents.length; i++) {
		hideContent(contents[i]);
	}

	var errors = getElementsByTagAndClassName("td","stderr");
	for (var i = 0; i < errors.length; i++) {
		hideContent(errors[i]);
	}

	var commands = getElementsByTagAndClassName("td","command");
	for (var i = 0; i < commands.length; i++) {
		hideContent(commands[i]);
	}

   forEach(getElementsByTagAndClassName("tr","stage-row"),
	   function (element) {
	      var stage_id = element.id.split("-")[1];
	      stageIds.push(stage_id);
	   }
	   );

   var autorun = $('autorun');
   if (autorun) {
      if (autorun.value == 'autorun') {
	 runAllStages();
      }
   }
}

addLoadEvent(initPush);

