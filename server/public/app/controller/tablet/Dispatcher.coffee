Ext.define "HomeSec.controller.tablet.Dispatcher",
  requires: "HomeSec.store.SStatus"
  config:
    stores:["SStatus"]
  extend: "Ext.app.Controller"
  init: ()->
    console.log "Controller Up"
    @callParent(arguments)
