import r2cloud.api
import r2cloud.tools.common
import sqlite3
import setting
import os.path
from db import db
from pluginManager import pluginManager

database = db("main", autoOpenClose = False)
plugins  = pluginManager(setting.plugins)
database.open()

for groundStation in setting.groundStations:
    api = r2cloud.api(groundStation['addr'])
    api.login(groundStation['user'], groundStation['pass'])
    
    # observations sync
    for ob in api.observationList():

        print("[INFO] sync observation %i from station %s" % (ob.id, groundStation['name']))

        # download A
        if setting.syncA and hasattr(ob.details(), 'aURL'):
            filename = "static/a/" + str(database.getUniqId(ob, groundStation)) + ".jpg"
            if not(os.path.isfile(filename)):
                print("[INFO] sync %i from station %s Download a" % (ob.id, groundStation['name']))
                image = ob.details().a()
                r2cloud.tools.common.bin2file(image, filename)

        # download data
        if setting.syncData and hasattr(ob.details(), 'dataURL'):
            filename = "static/bins/" + str(database.getUniqId(ob, groundStation)) + ".bin"
            if not(os.path.isfile(filename)):
                print("[INFO] sync %i from station %s Download data" % (ob.id, groundStation['name']))
                binary = ob.details().data()
                r2cloud.tools.common.bin2file(binary, filename)

        # download spectrogram
        if setting.syncSpectrograms and hasattr(ob.details(), 'spectrogramURL'):
            filename = "static/spectrograms/" + str(database.getUniqId(ob, groundStation)) + ".png"
            if not(os.path.isfile(filename)):
                print("[INFO] sync %i from station %s Download spectrogram" % (ob.id, groundStation['name']))
                spectrogram = ob.details().spectrogram()
                r2cloud.tools.common.bin2file(spectrogram, filename)

        # download raw
        if setting.syncRaws:
            if ob.name in ["NOAA 18", "NOAA 19", "NOAA 15"]:
                filename = "static/raws/" + str(database.getUniqId(ob, groundStation)) + ".wav"
            else:
                filename = "static/raws/" + str(database.getUniqId(ob, groundStation)) + ".raw.gz"

            if not(os.path.isfile(filename)):
                print("[INFO] sync %i from station %s Download raw" % (ob.id, groundStation['name']))
                raw = ob.details().raw()
                r2cloud.tools.common.bin2file(raw, filename)
                plugins.onDownloadRaw(ob, filename)

        try:
            database.insertObservation(ob, groundStation)

        except sqlite3.IntegrityError:
            database.updateObservation(ob, groundStation)

    # satelites SCHEDULES sync
    scheduleList = api.scheduleList()
    for sh in scheduleList:   
        
        print("[INFO] sync schedule %s from station %s" % (sh.id, groundStation['name']))

        try:
            database.insertSchedule(sh, groundStation)

        except sqlite3.IntegrityError:
            database.updateSchedule(sh, groundStation)

    # satelites sync
    tles = api.tle()
    for sh in scheduleList:
        try:
            print("[INFO] sync satellite %s" % (sh.id))

            tle = r2cloud.tools.common.tleFilterSat(tles, sh.name).tle[0]

            try:
                database.insertSatellite(
                    id         = sh.id,
                    name       = sh.name,
                    tle1       = tle.line1,
                    tle2       = tle.line2,
                    tle3       = tle.line3,
                    lastUpdate = tles.lastUpdated
                )

            except sqlite3.IntegrityError:
                database.updateSatellite(
                    id         = sh.id,
                    name       = sh.name,
                    tle1       = tle.line1,
                    tle2       = tle.line2,
                    tle3       = tle.line3,
                    lastUpdate = tles.lastUpdated
                )
        except:
            print("[INFO] fail to sync satellite %s - %s" % (sh.id, sh.name))

database.close()