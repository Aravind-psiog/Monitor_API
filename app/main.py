from cgitb import handler
from fastapi import FastAPI

from database import models
from database.database import engine
from routers import users, members, servers, authentication
from mangum import Mangum


models.Base.metadata.create_all(bind=engine)

# only used for aws for loading Swagger doc. Doesnot work on windows
app = FastAPI(root_path="/dev/")
# app = FastAPI()


@app.get('/')
def root():
    return {"message": "Hello from AWS"}


app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(members.router)
app.include_router(servers.router)
handler = Mangum(app)
