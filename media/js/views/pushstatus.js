define([
    'jquery',
    'underscore',
    'backbone'
], function ($, _, Backbone) {
    var PushStatusView = Backbone.View.extend({
        template: _.template($('#push-status-template').html()),
        el: $('#ps-app'),

        initialize: function () {
            this.model.bind('change', this.render, this);
        },

        render: function () {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        }
    });
    return PushStatusView;
});
