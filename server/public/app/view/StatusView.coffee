Ext.define "HomeSec.view.StatusView",
  requires: "HomeSec.store.SStatus"
  extend: "Ext.dataview.List"
  xtype: 'statusview'
  config:
   store: Ext.create 'HomeSec.store.SStatus'
   itemTpl: '<div class="myitem">{nameText} has tripped {tripValue} times </div>'
  constructor: ()->
    console.log "Loaded StatusView"
    @callParent(arguments)