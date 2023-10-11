import os
import importlib.util
import sys

from typing import Annotated
from fastapi import APIRouter, UploadFile, File
from server.models.microservices import Microservice
from server.models.microservices import FileContent
from server.database import microservices_collection
from server.schemas.schemas import list_microservices_serial
from parsing_modules.microservice_extractor import extract_microservice

# Used for fetching Mongo objectID
from bson import ObjectId, json_util

router = APIRouter()

# pipes_list GET


@router.get("/microservice/list")
async def get_microservices():
    microservices = list_microservices_serial(microservices_collection.find())
    return microservices


@router.post("/microservice/add")
async def add_microservice(microservice: Microservice):
    _id = microservices_collection.insert_one(dict(microservice))
    print("id", _id.inserted_id, _id.inserted_id.__str__())
    return json_util.dumps({"id": _id.inserted_id.__str__()}, indent=4)


@router.put("/microservice/{id}")
async def edit_microservice(id: str, microservice: Microservice):
    microservices_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(microservice)})


@router.delete("/microservice/{id}")
async def delete_microservice(name: str):
    microservices_collection.find_one_and_delete(
        {"_id": ObjectId(id)})


@router.delete("/clear/microservices")
async def clear_all_microservices():
    microservices_collection.drop()


@router.post("/upload")
async def upload_microservice(file: FileContent):
    filepath = f"data/{file.filename}"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Need to test with empty/invalid files error handling
    with open(filepath, 'w+') as f:
        f.write(file.content)

    res_json = extract_microservice(file.filename.split('.')[0])

    return res_json


@router.post("/upload_csv")
async def upload_CSV(file: FileContent):
    filepath = f"data/{file.filename}"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Need to test with empty/invalid files error handling
    with open(filepath, 'w+') as f:
        f.write(file.content)
