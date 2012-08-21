// Generated by IcedCoffeeScript 1.3.3d
(function() {
  var NetServer, Observable, net,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  Observable = require("./Observable");

  net = require("net");

  NetServer = (function(_super) {

    __extends(NetServer, _super);

    function NetServer() {
      var server,
        _this = this;
      NetServer.__super__.constructor.apply(this, arguments);
      server = net.createServer(function(conn) {
        return _this.connect(conn, 'end', _this.connectionLost);
      });
      server.listen(4000, '127.0.0.1');
    }

    NetServer.prototype.connectionLost = function() {
      return console.log("Connection end");
    };

    return NetServer;

  })(Observable);

  global.exports = module.exports = NetServer;

}).call(this);