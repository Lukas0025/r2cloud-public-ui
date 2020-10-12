import sqlite3
from datetime import datetime
from datetime import timezone 
import json

class db():
    def __init__(self, file, autoOpenClose = True):
        self.file   = file
        self.autoIO = autoOpenClose

    def dictFactory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        
        return d

    def open(self, byAuto = False):
        if not(byAuto) or self.autoIO:
            self.conn             = sqlite3.connect(self.file)
            self.curs             = self.conn.cursor()
            self.curs.row_factory = self.dictFactory

    def close(self, byAuto = False):
        if not(byAuto) or self.autoIO:
            self.conn.commit()
            self.conn.close()

    def scheduleList(self):
        self.open(True)
        
        self.curs.execute('SELECT * FROM schedule')
        res = self.curs.fetchall()

        self.close(True)

        return res

    def planedPassList(self):
        self.open(True)

        dt = datetime.now() 
        
        utc_time = dt.replace(tzinfo = timezone.utc)
        utc_timestamp = utc_time.timestamp() 
        
        self.curs.execute('SELECT id, passStart as start, passEnd as end, name, -1 as hasData FROM schedule WHERE (passStart is not NULL) AND (passStart > ?) ORDER BY start DESC', (utc_timestamp,))
        res = self.curs.fetchall()

        self.close(True)

        return res

    def planedPassListOfGroundStation(self, gr):
        self.open(True)

        dt = datetime.now() 
        
        utc_time = dt.replace(tzinfo = timezone.utc)
        utc_timestamp = utc_time.timestamp() 
        
        self.curs.execute('SELECT id, passStart as start, passEnd as end, name, -1 as hasData FROM schedule WHERE (passStart is not NULL) AND (passStart > ?) AND groundStation = ? ORDER BY start DESC', (utc_timestamp, gr,))
        res = self.curs.fetchall()

        self.close(True)

        return res

    def deleteAllObesrvationsOlder(self, time):
        self.open(True)

        dt = datetime.now() 
        
        utc_time = dt.replace(tzinfo = timezone.utc)
        utc_timestamp = utc_time.timestamp() - time
        
        self.curs.execute('DELETE FROM observations WHERE start < ?', (utc_timestamp,))

        self.close(True)
        
    def activeScheduleList(self):
        self.open(True)
        
        self.curs.execute('SELECT * FROM schedule WHERE enabled = 1')
        res = self.curs.fetchall()

        self.close(True)

        return res

    def activeSatellites(self):
        self.open(True)
        
        self.curs.execute('SELECT * FROM schedule WHERE enabled = 1 GROUP BY satelliteId')
        res = self.curs.fetchall()

        self.close(True)

        return res

    def satellite(self, sat):
        self.open(True)
        
        self.curs.execute('SELECT * FROM satellites WHERE id = ? or name = ?', (sat, sat))
        res = self.curs.fetchone()

        self.close(True)

        return res


    def observationList(self, limit):
        self.open(True)
        
        self.curs.execute('SELECT id, tle1 as name, satellite as satelliteId, start, hasData FROM observations ORDER BY start DESC LIMIT ?', (limit,))
        res = self.curs.fetchall()

        self.close(True)

        return res

    def observationListOfGroundStation(self, gr, limit):
        self.open(True)
        
        self.curs.execute('SELECT id, tle1 as name, satellite as satelliteId, start, hasData FROM observations WHERE groundStation = ? ORDER BY start DESC LIMIT ?', (gr, limit,))
        res = self.curs.fetchall()

        self.close(True)

        return res

    def hasData(self, limit):
        self.open(True)
        
        self.curs.execute('SELECT id, tle1 as name, satellite as satelliteId, start, hasData FROM observations WHERE hasData = 1 ORDER BY start DESC LIMIT ?', (limit,))
        res = self.curs.fetchall()

        self.close(True)

        return res

    def observationListOfSat(self, sat, limit):
        self.open(True)
        
        self.curs.execute('SELECT id, tle1 as name, satellite as satelliteId, start, hasData FROM observations WHERE satellite = ? OR tle1 = ? ORDER BY start DESC LIMIT ?', (sat, sat, limit,))
        out = self.curs.fetchall()

        self.close(True)
        
        return out

    def sumOfDecodedPacketsInTime(self, time, timeRange):
        start = time - timeRange
        end   = time + timeRange

        self.open(True)
        
        self.curs.execute('SELECT SUM(numberOfDecodedPackets) as packetsNum FROM observations WHERE start >= ? AND end <= ?', (start, end))
        out = self.curs.fetchone()
        
        self.close(True)

        return out['packetsNum']

    def bestImageInTime(self, time, timeRange):
        start = time - timeRange
        end   = time + timeRange

        self.open(True)
        
        self.curs.execute('SELECT * FROM observations WHERE start >= ? AND end <= ? ORDER BY numberOfDecodedPackets DESC LIMIT 1', (start, end))
        out = self.curs.fetchone()
        
        self.close(True)

        return out

    def hasDataInTime(self, time, timeRange):
        start = time - timeRange
        end   = time + timeRange

        self.open(True)
        
        self.curs.execute('SELECT id, tle1 as name, satellite as satelliteId, start, hasData FROM observations WHERE start >= ? AND end <= ? AND hasData = 1', (start, end))
        out = self.curs.fetchall()
        
        self.close(True)

        return out
    
    def observationListInTime(self, time, timeRange, limit):
        start = time - timeRange
        end   = time + timeRange

        self.open(True)
        
        self.curs.execute('SELECT id, tle1 as name, satellite as satelliteId, start, hasData FROM observations WHERE start >= ? AND end <= ? ORDER BY start DESC LIMIT ?', (start, end, limit,))
        out = self.curs.fetchall()
        
        self.close(True)

        return out

    def observation(self, id):
        self.open(True)
        
        self.curs.execute('SELECT * FROM observations WHERE id = ?', (id,))
        res = self.curs.fetchone()

        self.close(True)

        return res

    def getUniqId(self, observation, groundStation):
        return int(str(groundStation['id']) + str(observation.id))

    def updateObservation(self, observation, groundStation):
                
        dataEntity = None

        if hasattr(observation.details(), 'dataEntity'):
            dataEntity = json.dumps(observation.details().dataEntity)

        self.open(True)
        self.curs.execute(
            'UPDATE observations SET satellite = ?, start = ?, end = ?, sampleRate = ?, inputSampleRate = ?, frequency = ?, actualFrequency = ?, decoder = ?, bandwidth = ?, tle1 = ?, tle2 = ?, tle3 = ?, numberOfDecodedPackets = ?, groundStation = ?, gain = ?, biast = ?, dataEntity = ?, hasData = ? WHERE id = ?',
            (
                observation.details().satellite,
                datetime.timestamp(observation.details().start),
                datetime.timestamp(observation.details().end),
                observation.details().sampleRate,
                observation.details().inputSampleRate,
                observation.details().frequency,
                observation.details().actualFrequency,
                observation.details().decoder,
                observation.details().bandwidth,
                observation.details().tle.line1,
                observation.details().tle.line2,
                observation.details().tle.line3,
                observation.details().numberOfDecodedPackets,
                groundStation['id'],
                observation.details().gain,
                observation.details().biast,
                dataEntity,
                observation.hasData,
                self.getUniqId(observation, groundStation)
            )
        )
        self.close(True)

    def insertObservation(self, observation, groundStation):
        
        dataEntity = None

        if hasattr(observation.details(), 'dataEntity'):
            dataEntity = json.dumps(observation.details().dataEntity)

        self.open(True)
        self.curs.execute(
            'INSERT INTO observations (satellite, start, end, sampleRate, inputSampleRate, frequency, actualFrequency, decoder, bandwidth, tle1, tle2, tle3, numberOfDecodedPackets, groundStation, gain, biast, dataEntity, hasData, id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (
                observation.details().satellite,
                datetime.timestamp(observation.details().start),
                datetime.timestamp(observation.details().end),
                observation.details().sampleRate,
                observation.details().inputSampleRate,
                observation.details().frequency,
                observation.details().actualFrequency,
                observation.details().decoder,
                observation.details().bandwidth,
                observation.details().tle.line1,
                observation.details().tle.line2,
                observation.details().tle.line3,
                observation.details().numberOfDecodedPackets,
                groundStation['id'],
                observation.details().gain,
                observation.details().biast,
                dataEntity,
                observation.hasData,
                self.getUniqId(observation, groundStation)
            )
        )
        self.close(True)

    def clearSchedulePass(self, id):
        self.open(True)
        self.curs.execute('UPDATE schedule SET passStart = NULL, passEnd = NULL WHERE id = ?', (id))
        self.close(True)     

    def updateSchedulePass(self, id, newPass):
        self.open(True)
        self.curs.execute(
            'UPDATE schedule SET passStart = ?, passEnd = ? WHERE id = ?',
            (
                datetime.timestamp(newPass[0]),
                datetime.timestamp(newPass[2]),
                id
            )
        )
        self.close(True)     

    def insertSchedule(self, schedule, groundStation):
        self.open(True)
        self.curs.execute(
            'INSERT INTO schedule (id, satelliteId, name, enabled, frequency, groundStation) VALUES (?, ?, ?, ?, ?, ?)',
            (
                self.getUniqId(schedule, groundStation),
                schedule.satelliteId,
                schedule.name,
                schedule.enabled,
                schedule.frequency,
                groundStation['id']
                
            )
        )
        self.close(True)   

    def updateSchedule(self, schedule, groundStation):
        self.open(True)
        self.curs.execute(
            'UPDATE schedule SET satelliteId = ?, name = ?, enabled = ?, frequency = ?, groundStation = ? WHERE id = ?',
            (
                schedule.satelliteId,
                schedule.name,
                schedule.enabled,
                schedule.frequency,
                groundStation['id'],
                self.getUniqId(schedule, groundStation)
            )
        )
        self.close(True)        

    def insertSatellite(self, id, name, tle1, tle2, tle3, lastUpdate):
        self.open(True)
        self.curs.execute(
            'INSERT INTO satellites (id, name, tle1, tle2, tle3, lastUpdate) VALUES (?, ?, ?, ?, ?, ?)',
            (
                id,
                name,
                tle1,
                tle2,
                tle3,
                datetime.timestamp(lastUpdate)
                
            )
        )
        self.close(True)   

    def updateSatellite(self, id, name, tle1, tle2, tle3, lastUpdate):
        self.open(True)
        self.curs.execute(
            'UPDATE satellites SET name = ?, tle1 = ?, tle2 = ?, tle3 = ?, lastUpdate = ? WHERE id = ?',
            (
                name,
                tle1,
                tle2,
                tle3,
                datetime.timestamp(lastUpdate),
                id
            )
        )
        self.close(True)    



