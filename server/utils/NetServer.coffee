Observable = require "../shared/Observable"
net = require "net"
class NetServer extends Observable
  constructor:()->
    super
    server = net.createServer (conn)=>
      @connect conn, 'end', @connectionLost
      
    server.listen 4000, '127.0.0.1'
  
  connectionLost: ()->
    console.log "Connection end"
    
global.exports = module.exports = NetServer


