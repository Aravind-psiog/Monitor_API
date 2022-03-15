from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
import crud
from database.database import get_db
from sqlalchemy.orm import Session
import schemas
from managers.hashmanager import verify_hash
import managers.tokenmanager
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from mangum import Mangum


router = APIRouter(
    tags=["Authentication"]
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    login=crud.login_user(request,db)
    if login:
        verified = verify_hash(request.password,login.password)
        if verified:
            
            access_token = managers.tokenmanager.create_access_token(data={"sub": login.email})
            return {"access_token": access_token, "token_type": "bearer"}
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "success": False, "data": jsonable_encoder(request), "message": f"Incorrect Password"})
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"success": True, "data": jsonable_encoder(
            request), "message": f"Invalid email address"})

handler = Mangum(router)