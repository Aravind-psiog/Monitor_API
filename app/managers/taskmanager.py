import os
from fastapi import FastAPI

app = FastAPI()


def ping_server(ip_address: str):
    response = os.system("ping " + ip_address)

    if response == 0:
        print(True)
        return True

    else:
        print(False)
        return False


def background(background_tasks, request, current_user, models, db):
    task = background_tasks.add_task(ping_server, request.ip_address)
