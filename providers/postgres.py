import os


def backup(address: str, port: int, user: str, password: str, database: str, out: str):
    if port is None:
        port = 5432
    auth = ""
    if password is not None:
        auth = f'PGPASSWORD="{password}" '
    os.system(
        f"{auth}pg_dump -h {address} -p {port} -Fc -o -U {user} {database} > {out}"
    )
