Ext.define "HomeSec.model.MStatus"
  extend: "Ext.data.Model"
  config:
    fields: [
        {
          name: "sensorValue"
          type: "int"
        }
        { 
          name: "sensorName"
          type: "string"
        }
        { 
          name: "sensorDescription"
          type: "string"
        }
        {
          name: "lastTripped",
          type: "string",
          convert:(value, record)->
            if value?
              d = new Date(value)
              Ext.Date.format(d, 'M-d, D h:s')
            else   
              null
        }
    ]
