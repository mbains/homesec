
class ScopedRouter
  constructor: (@app)->
  
  bindroute: (path, method, handler) ->
    @app[method] path, ()=>
      handler.apply @, arguments
      
module.exports = ScopedRouter