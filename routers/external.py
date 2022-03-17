from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from database.database import get_db
from sqlalchemy.orm import Session
import schemas
import requests
from configs import loadconfigs
from mangum import Mangum


router = APIRouter(
    prefix="/api/external",
    tags=["external"]
)

key = loadconfigs.read_config()["Keys"]["AccessKey"]


@router.get("/{ip}/{type}")
def external(ip, type):
    if type in ["basic", "medium", "full"]:
        try:
            print(type)
            if type == "basic":
                result = requests.get(
                    f"http://api.ipstack.com/{ip}?access_key={key}")
                return HTTPException(status_code=status.HTTP_200_OK, detail={
                    "success": True, "data": {"ip": result.json()["ip"], "type": result.json()["type"], "country_name": result.json()["country_name"], "zip": result.json()["zip"]}, "message": f"IP details"})
            elif type == "medium":
                result = requests.get(
                    f"http://api.ipstack.com/{ip}?access_key={key}")
                print(result.json())
                return HTTPException(status_code=status.HTTP_200_OK, detail={
                    "success": True, "data": {"ip": result.json()["ip"], "type": result.json()["type"], "country_name": result.json()["country_name"], "zip": result.json()["zip"], "location": result.json()["location"]}, "message": f"IP details"})
            result = requests.get(
                f"http://api.ipstack.com/{ip}?access_key={key}")
            return HTTPException(status_code=status.HTTP_200_OK, detail={
                "success": True, "data": result.json(), "message": f"IP details"})
        except Exception as e:
            return HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                "success": False, "data": ip, "message": f"Invalid IP Address"})
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
        "success": False, "data": ip, "message": f"Invalid parameter passed"})


handler = Mangum(router)
