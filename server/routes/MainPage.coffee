ScopedRouter = require "./ScopedRouter" 

class MainPage extends ScopedRouter
  constructor: ()->
    super
    console.log "MainPage " + @app
    @bindroute "/mainpage", 'get', @renderGet
  
  renderGet: (req, res)->
    res.send("OK")
    
    
global.exports = module.exports = MainPage
