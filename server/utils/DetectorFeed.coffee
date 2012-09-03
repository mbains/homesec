Observable = require "./shared/Observable"
SerialPort = (require "serialport").SerialPort

class DetectorFeed extends Observable
  constructor:->
    super
    @currentSockets = {}
    @tripCount = 0
    @lastTripped = Date.now()
    
    console.log "Creating DETECTOR FEED"
    @sockets.on "connection", (socket)=>
        console.log "Sending news: " + socket.id
        @currentSockets[socket.id] = socket
        socket.on "disconnect", ()=>
          console.log "socket disconnected:" + socket.id
          delete @currentSockets[socket.id]
        socket.on "getNews", ()=>
          @sendNews socket
        
        @sendNews socket
          
    
  startSerialPort: ()->
    port = new SerialPort "/dev/ttyACM0", baudrate:9600
    last = 0
    
    port.on 'data', (data)=>
      s = data.toString()
      status = parseInt (s.slice s.length - 2, s.length - 1)
      if status isnt last and status is 1
        @tripCount+=1
        @lastTripped = Date.now()
        @sendNews sock for id, sock of @currentSockets
      last = status
    timer = ()->
      port.write '~in0D~'
    setInterval timer, 1000
    
    
  sendNews:(socket)->
    socket.emit "news", {
      sensorName: "motionsensor", 
      sensorValue: @tripCount,
      lastTripped: @lastTripped}
        

  
      
global.exports = module.exports = DetectorFeed