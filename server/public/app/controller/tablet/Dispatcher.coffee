Ext.define "HomeSec.controller.tablet.Dispatcher",
  requires: "HomeSec.controller.DispatcherMain"
  extend: "HomeSec.controller.DispatcherMain"
  init: ()->
    console.log "Controller Up"
    @callParent(arguments)
