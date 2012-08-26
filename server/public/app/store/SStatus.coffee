Ext.define "HomeSec.store.SStatus",
  requires: "HomeSec.model.MStatus"
  extend: "Ext.data.Store"
  config:
    #model: "HomeSec.model.MStatus"
    fields: [
        {
          name: "tripValue"
          type: "int"
        }
        { 
          name: "nameText"
          type: "string"
        }
    ]
    data: [
      {tripValue: 5, nameText: "Motion Sensor"}
    ]
    