Ext.Loader.setConfig enabled:true, disableCaching:false

Ext.application
  requires: ["Ext.event.Dispatcher"]
  name: "HomeSec"
  profiles: ["Tablet"]
  launch: ()->
    console.log "APP launch"
  


