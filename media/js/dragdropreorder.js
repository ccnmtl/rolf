var dragging;
var changed = false;

//document.captureEvents(Event.MOUSEMOVE);

function doDown(e) {
    if (e.target.name == "title") return true;
    document.onmousemove = doDrag;
    target = findDraggableParent(e.target);
    if (target == null) return;
    dragging = target;
    addElementClass(dragging,"dragging");
    return false;
}

function findDraggableParent(el) {
    if (el == null) return null;
    else if (hasElementClass(el,"draggable")) return el;
    else return findDraggableParent(el.parentNode);
}

function doDrag(e) {
    if (!dragging) return;
    target = findDraggableParent(e.target);
    if (target == null) return;
    if (target.id != dragging.id) {
        swapElements(target, dragging);
	changed = true;
    }
    return false;
}

function swapElements(child1, child2) {
    var parent = child1.parentNode;
    var children = parent.childNodes;
    var items = new Array();
    for (var i = 0; i < children.length; i++) {
        items[i] = children.item(i);
        if (children.item(i).id) {
            if (children.item(i).id == child1.id) items[i] = child2;
            if (children.item(i).id == child2.id) items[i] = child1;
        }
    }
    for (var i = 0; i < children.length; i++) {
        parent.removeChild(children.item(i));
    }
    for (var i = 0; i < items.length; i++) {
        parent.appendChild(items[i]);

    }
}

function doUp(e) {
    if (!dragging) return;
    removeElementClass(dragging,"dragging");
    addElementClass(dragging,"draggable");
    if (changed) {
        saveOrder();
    }

    dragging = null;
    document.onmousemove = null;
    changed = false;
    return false;
}

function debug(message) {
    t = document.createTextNode(message);
    $("debug").appendChild(t);
}

function saveOrder() {
    var ul = $("stages-table");
    var children = ul.childNodes;
    var idx = 1;
    var url = "reorder_stages/?";

    for (var i = 0; i < children.length; i++) {
        el = children.item(i);
        if (el.id) {
            if (el.id.indexOf("stage-") == 0) {
                id = el.id.substring(6);
                url += "stage_" + id + "=" + idx + ";";
                idx++;
            }
        }
    }
    var req = new XMLHttpRequest();
    req.open("GET",url,true);
    req.send(null);
}

document.onmousedown=doDown;
document.onmouseup=doUp;

