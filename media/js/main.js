require.config({
    paths: {
        // Major libraries
        jquery: 'jquery-1.9.1.min',
        underscore: 'libs/underscore/underscore-min',
        backbone: 'libs/backbone/backbone-1.0.0-min',

        // Require.js plugins
        text: 'libs/require/text',
        order: 'libs/require/order'
    },
    urlArgs: 'bust=' +  (new Date()).getTime(),
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

require(['views/app'], function(App) {
    window.appView = new App();
});
