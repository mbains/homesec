#TODO: Figure out why DispatcherMain is not included in build
Ext.application
  name: "HomeSec"
  requires: "HomeSec.controller.DispatcherMain"
  profiles: ["Tablet"]
  controllers: ["DispatcherMain"]
  launch: ()->
    console.log "APP launch"
  


