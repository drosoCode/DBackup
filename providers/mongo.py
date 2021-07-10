import os


def backup(address: str, port: int, user: str, password: str, database: str, out: str):
    if port is None:
        port = 27017
    auth = ""
    if user is not None:
        auth += f" -u {user}"
    if password is not None:
        auth += f" -p {password}"
    os.system(
        f"mongodump --db {database} --host {address} --port {port}{auth} -o {out}"
    )
