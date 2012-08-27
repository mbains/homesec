Ext.define "HomeSec.store.SStatus",
  requires: "HomeSec.model.MStatus"
  extend: "Ext.data.Store"
  config:
    model: "HomeSec.model.MStatus"
    data: [
      {
        sensorValue: 5
        sensorName: "motionsensor"
        sensorDescription: "Motion Sensor"
      }
    ]
    
