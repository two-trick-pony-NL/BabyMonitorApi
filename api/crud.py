import os
import time
import boto3
from typing import Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from boto3.dynamodb.conditions import Key
import random

app = FastAPI()
handler = Mangum(app)


#Model of what we store in database
class NewSnapShot(BaseModel):
    cryDetected: bool = False
    soundDetected: bool = False
    movementDetected: bool = False
    shouldNotifyClient: bool = False
    lastUpdate: int
    userId: str


@app.get("/")
async def root():
    randomnumber = random.randint(3, 9)
    return {"A random Number": randomnumber}


@app.put("/create-measurement")
async def create_Measurement(new_snapshot: NewSnapShot):
    created_time = int(time.time())
    item = {
        "cryDetected": new_snapshot.cryDetected,
        "soundDetected": new_snapshot.soundDetected,
        "movementDetected": new_snapshot.movementDetected,
        "shouldNotifyClient": new_snapshot.shouldNotifyClient,
        "lastUpdate": created_time,
        "userId": new_snapshot.userId,
        "measurementId": f"measurement_{uuid4().hex}",
    }

    # Put it into the table.
    table = _get_table()
    table.put_item(Item=item)
    return {"measurement": item}


@app.get("/get-measurement/{measurementId}")
async def get_measurement(measurementId: str):
    # Get the measurement from the table.
    table = _get_table()
    response = table.get_item(Key={"measurementId": measurementId})
    item = response.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail=f"measurement {measurementId} not found")
    return item


@app.get("/list-measurements/{user_id}")
async def list_measurements(userId: str):
    # List the top N measurements from the table, using the user index.
    table = _get_table()
    response = table.query(
        IndexName="user-index",
        KeyConditionExpression=Key("userId").eq(userId),
        ScanIndexForward=False,
        Limit=10,
    )
    measurements = response.get("Items")
    return {"measurements": measurements}

@app.delete("/delete-measurement/{measurementId}")
async def delete_measurement(measurementId: str):
    # Delete the measurement from the table.
    table = _get_table()
    table.delete_item(Key={"measurementId": measurementId})
    return {"deleted_measurement_id": measurementId}


def _get_table():
    #table_name = os.environ.get("TABLE_NAME")
    table_name = "babyMonitorApi-MeasurementsF277F0E3-BK380OWVLBTN"
    return boto3.resource("dynamodb").Table(table_name)
