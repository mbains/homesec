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
    ]
