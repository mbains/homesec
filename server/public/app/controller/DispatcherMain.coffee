console.log "file included"
Ext.define "HomeSec.controller.DispatcherMain",
  requires: ["HomeSec.store.SStatus",
             "HomeSec.model.MStatus",
             "HomeSec.utils.WebSocket"]
  config:
    stores:["SStatus"]
    models:["MStatus"]
  extend: "Ext.app.Controller"
  init: ()->
    window.cont = @
    console.log "DispatcherMain Up"
    @socket = window.thesocket
    @callParent(arguments)
    
  launch:()->
    console.log @socket
    @socket.onSignal signal: "news", fn: (news)->
      store = Ext.getStore("SStatus")
      r = store.findRecord "sensorName", news.sensorName
      console.log "Found: " + r
      r.set "sensorValue", news.sensorValue
      r.set "lastTripped", news.lastTripped
      console.log "Here's the news: #{news.sensorName}"
      
    @socket.io.emit "getNews"
