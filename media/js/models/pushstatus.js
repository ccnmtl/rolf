define([
    'backbone'
], function (Backbone) {
    var PushStatus = Backbone.Model.extend({
        defaults: {
            'status': 'inprogress'
        }
    });
    return PushStatus;
});
