import os


def backup(address: str, port: int, user: str, password: str, database: str, out: str):
    if port is None:
        port = 3306
    auth = ""
    if password is not None:
        auth = f'MYSQL_PWD="{password}" '
    os.system(f"{auth}mysqldump --host={address} -P {port} {database} > {out}")