from database import models


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
