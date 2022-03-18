from database import models
from sqlalchemy import exc
from datetime import datetime


def create_server_group(request, db, current_user):
    server_group = request.server_group.lower()
    user = db.query(models.UserItems).get(current_user.email)
    server_member = models.GroupItems(email=current_user.email, created_on=datetime.now(
    ), username=user.username, server_group=server_group, admin=True)
    server_group = models.ServerGroup(
        created_on=datetime.now(), server_group=server_group)
    db.add(server_group)
    try:
        db.commit()
        db.add(server_member)
        db.commit()

        return True
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
