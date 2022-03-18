from database import models
from sqlalchemy import exc
from datetime import datetime
import uuid
from managers import hashmanager


def create_user(request, db):
    hashed_password = hashmanager.hash_password(request.password1)
    new_user = models.UserItems(
        email=request.email, created_on=datetime.now(), username=request.username, password=hashed_password)
    db.add(new_user)
    try:
        db.commit()
        return True
    except exc.IntegrityError:
        return False


def get_users(db, email):
    users = db.query(models.UserItems).filter(
        models.UserItems.email != email).all()
    return users


def invite_user(request, db, current_user):
    code = str(uuid.uuid4())
    invited_to = request.invited_to.lower()
    try:
        check = db.query(models.UserItems).filter(
            models.UserItems.email.like(request.user)).one()
    except:
        return 2
    try:
        db.query(models.GroupItems).filter(models.GroupItems.email.like(
            current_user.email), models.GroupItems.server_group.like(invited_to)).one()
    except Exception as e:
        return 0
    invite_user_read = db.query(models.InviteItems).filter(
        models.InviteItems.user == request.user).all()
    for users in invite_user_read:
        if users.user == request.user and users.invited_to == invited_to:
            return 1
    invite_user = models.InviteItems(
        invited_by=current_user.email, invited_on=datetime.now(), invited_to=invited_to, user=request.user, code=code[:8])
    db.add(invite_user)
    try:
        db.commit()
        return {"code": code[:8]}
    except exc.IntegrityError:
        return False


def list_member(group, db, current_user):
    try:
        server_member = db.query(models.GroupItems).filter(models.GroupItems.email.like(
            current_user.email), models.GroupItems.server_group.like(group.lower())).one()
    except Exception as e:
        return False
    if server_member:
        server_member = db.query(models.GroupItems).filter(models.GroupItems.email.notlike(
            current_user.email), models.GroupItems.server_group.like(group.lower())).all()
        return server_member
    return False
