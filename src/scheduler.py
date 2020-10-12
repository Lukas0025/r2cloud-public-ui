from pyorbital.orbital import Orbital
from datetime import datetime
from db import db
import setting

database = db("main", autoOpenClose = False)
database.open()

for sh in database.activeScheduleList():

    sat       = database.satellite(sh['satelliteId'])
    pyOrbital = Orbital(sat["tle1"], line1=sat["tle2"], line2=sat["tle3"])
        
    utctime = datetime.utcnow()

    gr = sh['groundStation']

    passes = pyOrbital.get_next_passes(
        utctime,
        24,
        setting.groundStations[gr]["lon"],
        setting.groundStations[gr]["lat"], 
        setting.groundStations[gr]["alt"], 
        tol=0.001
    )

    if len(passes) > 0:
        print("[INFO] new pass for satellite %s - %s" % (sh['id'], passes[0][0].strftime("%m/%d/%Y, %H:%M:%S")))
        database.updateSchedulePass(sh['id'], passes[0])

    else:
        print("[INFO] no new pass for satellite %s" % (sh['id']))
        database.clearSchedulePass(sh['id'])

database.close()

        