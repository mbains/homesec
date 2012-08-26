
class Observable
  constructor: (config)->
    @[key]=value for own key, value of config
    
  connect:(onObj, signal, fn)->
    extraArgs = [].splice.call arguments,3
    onObj.on signal, ()=>
      argsList = [].splice.call arguments, 0
      argsList = argsList.concat extraArgs
      fn.apply @, argsList
      
global.exports = module.exports = Observable