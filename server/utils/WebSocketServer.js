// Generated by IcedCoffeeScript 1.3.3d
var Observable, WebSocketServer, net, sock,
  __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

Observable = require("./shared/Observable");

sock = require('socket.io');

net = require("net");

WebSocketServer = (function(_super) {

  __extends(WebSocketServer, _super);

  function WebSocketServer() {
    WebSocketServer.__super__.constructor.apply(this, arguments);
    this.handlers = [];
    this.io = sock.listen(this.server);
    this.connect(this.io.sockets, 'connection', this.browserConnected);
  }

  WebSocketServer.prototype.browserConnected = function(socket) {
    return console.log("Browser Connected");
  };

  WebSocketServer.prototype.createHandler = function(klass) {
    console.log("creating Handler " + klass);
    return this.handlers.push(new klass({
      io: this.io,
      sockets: this.io.sockets
    }));
  };

  return WebSocketServer;

})(Observable);

global.exports = module.exports = WebSocketServer;