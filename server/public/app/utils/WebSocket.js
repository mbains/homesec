Ext.define('HomeSec.utils.WebSocket', {
    extend: 'Ext.util.Observable',
    singleton: true,
    constructor: function(config) {
        console.log('WebSocket created');
        window.thesocket = this;
        this.initConfig(config);
        this.callParent(arguments);
        this.init();
    },
    init: function() {
        var me = this;
        this.io = io.connect(window.location.origin);
        this.io.on('connect', function() {
            me.fireEvent('connected');
        });
        this.io.on('disconnect', function() {
            me.fireEvent('disconnected');
        });
    },
    //a better dispatcher than what socket.io provides
    onSignal: function(opts) {
        if(typeof opts !== 'object' || typeof opts.signal !== 'string' || typeof opts.fn !== 'function') {
            Ext.Error.raise('Need config option with "signal"(string) and "fn"(function)');
        }
        //NOTE: When changing function arguments, update hard coded index below
        var extraArgs = [].splice.call(arguments,1); 
        this.io.on(opts.signal, function() {
            var argList = [].splice.call(arguments, 0)
            if(extraArgs.length) {
                argList = argList.concat(extraArgs)
            }
            opts.fn.apply(opts.scope, argList);
        });
    }
    
});

