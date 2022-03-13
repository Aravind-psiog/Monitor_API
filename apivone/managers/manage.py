import os


def manual_check(ip_address):
    response = os.system("ping " + ip_address)

    if response == 0:
        print(True)
        return True

    else:
        print(False)
        return False
