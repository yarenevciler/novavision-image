import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import uvicorn
from fastapi import FastAPI,Request
#from pydantic import BaseModel
import json

from capsules.capTrafficSignClassifier.src.executors.TrafficSign import TrafficInferrer
from sdks.novavision.src.base.service import Service
from sdks.novavision.src.base.bootstrap import Bootstrap
app = FastAPI()


executors = {'Traffic':{"Traffic":TrafficInferrer}}

btstrp = Bootstrap(executors)
bootstrap = btstrp.run()

#class JsonPayload(BaseModel):
    #data :dict
#@app.post("/receive")
#def receive_json(payload: JsonPayload):
    #try:
        #with open("received_payload.json","w") as json_file:
            #json.dump(payload.data, json_file, indent = 4)
        #return{"message":"JSON verisi kaydedildi."}
    #except Exception as e:
        #raise HTTPException(status_code = 500, detail= str(e))

@app.post('/api')
async def api(request: Request):
    json_data = await request.json()
    json_data = json.dumps(json_data)
    resp = Service(json_data, executors, bootstrap).run()
    return resp


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
