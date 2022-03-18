import re
from database import models
from managers import manage


def get_server_group(current_user, db):
    server_member = db.query(models.GroupItems).filter(
        models.GroupItems.email == current_user.email).all()
    return server_member


def create_server(request, db, current_user):
    server_group = request.server_group.lower()
    check_member = db.query(models.GroupItems).filter(models.GroupItems.email.like(
        current_user.email), models.GroupItems.server_group.like(server_group)).first()
    if check_member:
        regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        if(re.search(regex, request.ip_address)):
            status = manage.manual_check(request.ip_address)
            new_user = models.ServerItems(
                server_group=server_group, created_by=current_user.email, ip_address=request.ip_address, online=status)
            db.add(new_user)
            db.commit()
            return 0
        return 1
    return 2
