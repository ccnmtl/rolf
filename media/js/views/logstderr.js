define([
    'jquery',
    'underscore',
    'backbone',
    'utils/hidecontent'
], function ($, _, Backbone, hideContent) {
    var LogStderrView = Backbone.View.extend({
        tagName: 'tr',
        template: _.template($('#stderr-template').html()),
        initialize: function () {
            this.model.bind('change', this.render, this);
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            if (this.model.get('result').get('status') === 'ok') {
                hideContent(this.$('td'));
            }
            return this;
        }
    });
    return LogStderrView;
});
