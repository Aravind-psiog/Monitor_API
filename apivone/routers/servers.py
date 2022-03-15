from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.encoders import jsonable_encoder
import crud
from database.database import get_db
from sqlalchemy.orm import Session
import schemas
from managers import tokenmanager
from mangum import Mangum

router = APIRouter(
    prefix="/api/server",
    tags=["server"]
)


@router.get('/list-server-group')
def list_server_group(db: Session = Depends(get_db), current_user: schemas.UserItems = Depends(tokenmanager.get_current_user)):
    get_groups = crud.get_server_group(current_user, db)
    if get_groups:
        raise HTTPException(status_code=status.HTTP_200_OK, detail={
                            "success": True, "message": "group details", "data": jsonable_encoder(get_groups)})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                        "success": False, "message": f"You have no group", "data": None})


@router.post('/create-server')
async def create_server(background_tasks: BackgroundTasks, request: schemas.ServerDetailsItems, db: Session = Depends(get_db), current_user: schemas.UserItems = Depends(tokenmanager.get_current_user)):
    create = crud.create_server(request, db, current_user)
    if create == 0:
        raise HTTPException(status_code=status.HTTP_200_OK, detail={"success": True, "data": jsonable_encoder(
            request), "message": f"Server {request.ip_address} added successfully"})
    elif create == 2:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
            "success": False, "data": jsonable_encoder(request), "message": f"Something went wrong"})
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
            "success": False, "data": jsonable_encoder(request), "message": f"Invalid IP address"})
