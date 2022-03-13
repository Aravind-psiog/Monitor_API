from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
import crud
from database.database import get_db
from sqlalchemy.orm import Session
import schemas
from managers import tokenmanager
from mangum import Mangum

router = APIRouter(
    prefix="/api/member",
    tags=["member"]
)


@router.post('/create-group')
def create_group(request: schemas.ServerItems, db: Session = Depends(get_db), current_user: schemas.UserItems = Depends(tokenmanager.get_current_user)):
    new_server = crud.create_server_group(request, db, current_user)
    if new_server:
        raise HTTPException(status_code=status.HTTP_200_OK, detail={"success": True, "data": jsonable_encoder(
            request), "message": f"Group {request.server_group} created successfully"})
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                        "success": False, "data": jsonable_encoder(request), "message": f"User {request.server_group} already exists. Use different name"})


@router.get('/accept-invite/{email}/{code}')
def accept_invite(code, email, db: Session = Depends(get_db)):
    check_invite = crud.accept_invite(code, email, db)
    if check_invite:
        raise HTTPException(status_code=status.HTTP_200_OK, detail={
                            "success": True, "data": email, "message": f"Invite accepted!"})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                        "success": False, "message": "Invalid or expired link", "data": None})

handler = Mangum(router)