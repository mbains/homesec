Observable = require "./shared/Observable"
SerialPort = (require "serialport").SerialPort

class DetectorFeed extends Observable
  constructor:->
    super
    @currentSockets = {}
    console.log "Creating DETECTOR FEED"
    @sockets.on "connection", (socket)=>
        console.log "Sending news: " + socket.id
        @currentSockets[socket.id] = socket
        socket.on "disconnect", ()=>
          console.log "socket disconnected:" + socket.id
          delete @currentSockets[socket.id]
        @sendNews socket, 42
    
  startSerialPort: ()->
    port = new SerialPort "/dev/ttyACM0", baudrate:9600
    last = 0
    tripCount = 0
    
    port.on 'data', (data)=>
      console.log "data: " + data
      s = data.toString()
      status = s.slice s.length - 2, s.length - 1
      if status is not last and status is 1
        tripCount+=1
        @sendNews sock, tripCount for id, sock of @currentSockets
        
    timer = ()->
      port.write '~in0D~'
    setInterval timer, 1000
    
    
  sendNews:(socket, value)->
    socket.emit "news", {sensorName: "motionsensor", sensorValue: value}
        

  
      
global.exports = module.exports = DetectorFeed