from flask import Flask,request,jsonify
from flask_swagger import swagger
from datetime import  datetime
import json as js

from dotenv import dotenv_values
JSON_PATH = dotenv_values(".env")["JSON_FILE"]
print(JSON_PATH)

app = Flask(__name__)

def find_device_index(devices,device_id):
    for i,d in enumerate(devices):
        if d["id"] == device_id:
            return i
    raise Exception("device not found")
def find_key_index(params,key):
    for i,p in enumerate(params):
        if p["name"] == key:
            return i
    raise Exception("paramter not found")

@app.route("/update",methods=['POST'])
def update():
    payload= request.get_json()
    device_type = payload["device_type"]
    device_id = payload["device_id"]
    key = payload["key"]
    value = payload["value"]

    json_file = open("../ShrimpSoftware-1.0-Linux/json/hardware_devices_radio.json") 
    json_data = js.load(json_file)
    json_file.close()

    devices = json_data[device_type]
    device_index = find_device_index(devices,device_id)

    device_params = devices[device_index]["params"]
    param_index = find_key_index(device_params,key)

    json_data[device_type][device_index]["params"][param_index]['value'] = value

    json_file = open("../ShrimpSoftware-1.0-Linux/json/hardware_devices_radio.json","w+") 
    js_string = js.dumps(json_data,indent=4, separators=(',', ': '))
    json_file.write(js_string)
    json_file.close()
    

    return {
            "success":True,
    }

@app.route("/get/<device_type>/<id_device>/<key>",methods=['GET'])
def get_param(device_type,id_device,key):
    json_file = open("../ShrimpSoftware-1.0-Linux/json/hardware_devices_radio.json") 
    json_data = js.load(json_file)
    json_file.close()
    try:
        devices = json_data[device_type]
        device_index = find_device_index(devices,int(id_device))

        device_params = devices[device_index]["params"]
        param_index = find_key_index(device_params,key)

        value = json_data[device_type][device_index]["params"][param_index]['value'] 
        return {
            "success":True,
            "value":value
                } 

    except:
        return {
            "success":False,
            "value":None,
            "str_err":"could not find requested value"
                } 

if __name__=="__main__":
    app.run(debug=True)
