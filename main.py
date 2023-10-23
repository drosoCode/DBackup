#!/usr/local/bin/python3

import yaml
import croniter
import datetime
import time
from importlib import import_module
import os
import shutil


def importProvider(src: str):
    if not os.path.exists("providers/" + src + ".py"):
        print(f"unknown provider {src}")
        return None
    return import_module("providers." + src)


def backupDatabases(providers, databases, basePath):
    for i in databases:
        if i["enabled"]:
            try:
                if "before" in i:
                    os.system(i["before"])
                for j in i["database"].keys():
                    out = os.path.join(basePath, i["database"][j])
                    if "/" in out:
                        os.system(f"mkdir -p {out[0:out.rfind('/')]}")
                    print(f"backing up {j} to {out}")
                    providers[i["type"]].backup(
                        address=i.get("address"),
                        user=i.get("user"),
                        password=i.get("password"),
                        port=i.get("port"),
                        database=j,
                        out=out,
                    )
                if "after" in i:
                    os.system(i["after"])
            except Exception as e:
                print("failed with error:", e)


def backup(providers, config):
    if "before" in config["backup"]:
        os.system(config["backup"]["before"])

    folder = os.path.join(
        config["backup"]["folder"], datetime.datetime.now().strftime("%Y-%m-%d")
    )
    backupDatabases(providers, config["databases"], folder)

    if config["backup"].get("zip"):
        shutil.make_archive(folder, "zip", folder)
        shutil.rmtree(folder)

    if "max_items" in config["backup"]:
        backups = os.listdir(config["backup"]["folder"])
        if len(backups) > config["backup"]["max_items"]:
            sortedBackups = sorted(backups, reverse=True)
            for i in range(config["backup"]["max_items"], len(backups)):
                p = os.path.join(config["backup"]["folder"], sortedBackups[i])
                try:
                    shutil.rmtree(p)
                except NotADirectoryError:
                    os.remove(p)

    if "after" in config["backup"]:
        os.system(config["backup"]["after"])


with open("config.yml") as f:
    config = yaml.full_load(f)
    print("Configuration loaded")

providers = {}
for i in config["databases"]:
    if i["type"] not in providers:
        providers[i["type"]] = importProvider(i["type"])
print("loaded", len(providers), "providers")

cron = None
if config["settings"]["cron"] != "":
    cron = croniter.croniter(config["settings"]["cron"], datetime.datetime.now())
while True:
    # start a backup
    backup(providers, config)
    if cron is None:
        break
    # sleep until next occurrence
    nxt = cron.get_next(datetime.datetime)
    print("Next backup:", nxt)
    sleepTime = (nxt - datetime.datetime.now()).total_seconds()
    time.sleep(sleepTime)
