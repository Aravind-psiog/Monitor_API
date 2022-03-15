from pyexpat import model
import re
from database import models
from sqlalchemy import exc
from datetime import datetime
import uuid
from fastapi.encoders import jsonable_encoder
from managers import manage, hashmanager


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


def create_server_group(request, db, current_user):
    user = db.query(models.UserItems).get(current_user.email)
    server_member = models.GroupItems(email=current_user.email, created_on=datetime.now(
    ), username=user.username, server_group=request.server_group, admin=True)
    server_group = models.ServerGroup(
        created_on=datetime.now(), server_group=request.server_group)
    db.add(server_group)
    try:
        db.commit()
        db.add(server_member)
        db.commit()

        return True
    except exc.IntegrityError:
        return False


def get_server_group(current_user, db):
    server_member = db.query(models.GroupItems).filter(
        models.GroupItems.email == current_user.email).all()
    return server_member


def get_users(db, email):
    users = db.query(models.UserItems).filter(
        models.UserItems.email != email).all()
    return users


def invite_user(request, db, current_user):
    code = str(uuid.uuid4())
    try:
        check = db.query(models.UserItems).filter(
            models.UserItems.email.like(request.email)).one()
        print(jsonable_encoder(check))
    except:
        return 2
    try:
        db.query(models.GroupItems).filter(models.GroupItems.email.like(
            current_user.email), models.GroupItems.server_group.like(request.invited_to)).one()
    except Exception as e:
        print(e)
        return 0
    invite_user_read = db.query(models.InviteItems).filter(
        models.InviteItems.user == request.user).all()
    for users in invite_user_read:
        if users.user == request.user and users.invited_to == request.invited_to:
            return 1
    invite_user = models.InviteItems(
        invited_by=current_user.email, invited_on=datetime.now(), invited_to=request.invited_to, user=request.user, code=code[:8])
    db.add(invite_user)
    try:
        db.commit()
        return {"code": code[:8]}
    except exc.IntegrityError:
        return False


def accept_invite(code, email, db):
    check_invite = db.query(models.InviteItems).filter(
        models.InviteItems.user.like(email), models.InviteItems.code.like(code)).first()
    if check_invite:
        users = db.query(models.UserItems).filter(
            models.UserItems.email == email).first()
        server_member = models.GroupItems(email=email, username=users.username,
                                          server_group=check_invite.invited_to, admin=False, created_on=datetime.now())
        db.add(server_member)
        db.commit()
        obj = db.query(models.InviteItems).filter(models.InviteItems.user.like(
            email), models.InviteItems.code.like(code)).delete(synchronize_session=False)
        db.commit()
        return obj
    return False


def create_server(request, db, current_user):
    check_member = db.query(models.GroupItems).filter(models.GroupItems.email.like(
        current_user.email), models.GroupItems.server_group.like(request.server_group)).first()
    if check_member:
        regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        if(re.search(regex, request.ip_address)):
            status = manage.manual_check(request.ip_address)
            new_user = models.ServerItems(
                server_group=request.server_group, created_by=current_user.email, ip_address=request.ip_address, online=status)
            db.add(new_user)
            db.commit()
            return 0
        return 1
    return 2


def cron_get(db):
    storedb = []
    server_table = db.query(models.ServerItems)
    for server in server_table:
        storedb.append(server)
    db.close()
    return storedb


def cron_post(db, user_id, stat):

    server_member = db.query(models.ServerItems).filter(
        models.ServerItems.id == user_id).one()
    server_member.online = stat
    db.commit()
    db.close()


def login_user(request, db):
    login = db.query(models.UserItems).filter(
        models.UserItems.email == request.username).first()
    return login


def list_member(group, db, current_user):
    try:
        server_member = db.query(models.GroupItems).filter(models.GroupItems.email.like(
            current_user.email), models.GroupItems.server_group.like(group)).one()
    except Exception as e:
        print(e)
        return False
    if server_member:
        server_member = db.query(models.GroupItems).filter(models.GroupItems.email.notlike(
            current_user.email), models.GroupItems.server_group.like(group)).all()
        return server_member
    return False
