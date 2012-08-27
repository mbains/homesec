Ext.define "HomeSec.view.StatusView",
  requires: "HomeSec.store.SStatus"
  extend: "Ext.dataview.List"
  xtype: 'statusview'
  config:
   store: 'SStatus'
   itemTpl: '<div class="myitem">{sensorName} has tripped {sensorValue} times </div>'
  constructor: ()->
    console.log "Loaded StatusView"
    @callParent(arguments)
