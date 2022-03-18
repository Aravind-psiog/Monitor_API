from database import models


def login_user(request, db):
    login = db.query(models.UserItems).filter(
        models.UserItems.email == request.username).first()
    return login
