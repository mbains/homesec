
Ext.define "HomeSec.profile.Tablet",
  extend: "Ext.app.Profile"
  config:
    views:['MainView']
    controllers: ['Dispatcher']
  launch: ->
    Ext.create "HomeSec.view.tablet.MainView"
    console.log "Tablet Profile Launch"
    @callParent(arguments)
    
  isActive: ->
    true