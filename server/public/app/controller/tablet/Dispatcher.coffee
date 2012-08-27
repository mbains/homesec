Ext.define "HomeSec.controller.tablet.Dispatcher",
  extend: "HomeSec.controller.DispatcherMain"
  init: ()->
    console.log "Controller Up"
    @callParent(arguments)
