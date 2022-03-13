from sys import prefix
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
import crud
from database.database import get_db
from sqlalchemy.orm import Session
import schemas
from managers import tokenmanager
from mangum import Mangum


router = APIRouter(
    prefix = "/api/user",
    tags=["user"]
    )


@router.get('/list-users/')
def list_users(db: Session = Depends(get_db), current_user: schemas.UserItems = Depends(tokenmanager.get_current_user)):
    all_users = crud.get_users(db, current_user.email)
    if all_users:
        raise HTTPException(status_code=status.HTTP_200_OK, detail={
                            "success": True, "message": "Users list", "data": jsonable_encoder(all_users)})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                        "success": False, "message": "No Users to show yet", "data": None})


@router.post('/create-user')
def create_user(request: schemas.UserItems, db: Session = Depends(get_db)):
    new_user = crud.create_user(request, db)
    if new_user:
        raise HTTPException(status_code=status.HTTP_200_OK, detail={"success": True, "data": jsonable_encoder(
            request), "message": f"User {request.email} created successfully"})
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                        "success": False, "data": jsonable_encoder(request), "message": f"User {request.email} already exists"})


@router.post('/invite/')
def invite(request: schemas.InviteItems, db: Session = Depends(get_db), current_user: schemas.UserItems = Depends(tokenmanager.get_current_user)):
    invite = crud.invite_user(request, db, current_user)
    if invite:
        raise HTTPException(status_code=status.HTTP_200_OK, detail={"success": True, "data": jsonable_encoder(
            request), "message": f"Invite sent to {request.user}!"})
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                        "success": False, "data": jsonable_encoder(request), "message": f"Invite already sent to {request.user}"})


handler = Mangum(router)