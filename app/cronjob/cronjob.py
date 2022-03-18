import schedule
import time
import os
from configs.loadconfigs import read_config
from crud import cronjobs

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from fastapi.encoders import jsonable_encoder


engine = create_engine(read_config()["APP"]["DATABASE"])
db = scoped_session(sessionmaker(bind=engine))

json = jsonable_encoder


def job():
    server_table = cronjobs.cron_get(db)
    for servers in server_table:
        servers = (json(servers))
        ip_address = servers["ip_address"]
        user_id = (servers["id"])
        state = (servers["online"])  # false
        response = os.system("ping " + ip_address)

        if response == 0:
            print(True)
            if state != True:
                print("server is back online")
                cronjobs.cron_post(db, user_id, stat=True)

        else:
            print(False)
            if state != False:
                print("server is offline")
                cronjobs.cron_post(db, user_id, stat=False)


schedule.every(20).seconds.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
