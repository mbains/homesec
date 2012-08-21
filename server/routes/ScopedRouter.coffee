Observable = require "../Observable"

class ScopedRouter extends Observable
  constructor: (@app)->
    super
  
  bindroute: (path, method, handler) ->
    @app[method] path, ()=>
      handler.apply @, arguments
      
module.exports = ScopedRouter