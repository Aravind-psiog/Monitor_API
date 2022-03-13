import os
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def ping_server(ip_address:str):
    print("im pinging")
    response = os.system("ping " + ip_address)

    if response == 0:
        print(True)
        return True

    else:
        print(False)
        return False

def background(background_tasks, request, current_user,models,db):
    print("im at background")
    task = background_tasks.add_task(ping_server, request.ip_address)