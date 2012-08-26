Ext.define "HomeSec.view.tablet.MainView",
  requires: "HomeSec.view.StatusView"
  extend: "Ext.Panel"
  xtype: "mainview"
  config:
    layout: 
      type: "fit"
      pack: "center"
    fullscreen: true
    items:
      [xtype: 'statusview']
      
  constructor: ()->
    console.log "loading mainview"
    @callParent arguments
    
