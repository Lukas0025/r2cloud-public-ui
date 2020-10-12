import os
import setting
from db import db

# delete all a over TTL
if setting.aTTL > 0:
    os.system("find %s* -mtime +%s -exec rm \{\} \\;" % ("static/a/", setting.aTTL))

# delete all rows over TTL
if setting.rawsTTL > 0:
    os.system("find %s* -mtime +%s -exec rm \{\} \\;" % ("static/raws/", setting.rawsTTL))

# delete all raws over TTL
if setting.spectrogramsTTL > 0:
    os.system("find %s* -mtime +%s -exec rm \{\} \\;" % ("static/raws/", setting.spectrogramsTTL))

# delete all data over TTL
if setting.dataTTL > 0:
    os.system("find %s* -mtime +%s -exec rm \{\} \\;" % ("static/bins/", setting.dataTTL))

#delete all observations over TTL
if setting.observationTTL > 0:
    database = db("main")
    database.deleteAllObesrvationsOlder(setting.observationTTL * 86400)