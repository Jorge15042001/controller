
from flask import Flask,request,jsonify
from flask_swagger import swagger
from datetime import  datetime
import json as js


from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
ctx = app.app_context() # We are storing the context in a variable
ctx.push()


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)




class UpdateParamRequest(db.Model):
    __tablename__ = 'UpdateParamRequest'
    __table_args__ = { 'extend_existing': True }
    id_request = db.Column(db.Integer,primary_key = True, autoincrement=True)
    id_device= db.Column(db.String(50))
    file = db.Column(db.String(50))
    key = db.Column(db.String(50))
    valor = db.Column(db.String(50))

db.create_all()

#  @app.route("/get",methods=['GET'])
#  def get():
#      payload:dict = request.get_json()
#      file = payload["file"]
#      key = payload["key"]
#      #  value = payload["value"]
#
#      return {
#              "success":True,
#              "str_err":"",
#              "value":""
#      }


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

    device_params = devices[device_index]["hardware_params"]
    param_index = find_key_index(device_params,key)

    json_data[device_type][device_index]["params"][param_index]['value'] = value

    json_file = open("./datos.json","w+") 
    js_string = js.dumps(json_data,indent=4, separators=(',', ': '))
    json_file.write(js_string)
    json_file.close()
    

    return {
            "success":True,
    }


if __name__=="__main__":
    app.run(debug=True)
