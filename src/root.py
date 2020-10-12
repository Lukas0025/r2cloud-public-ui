import setting
import os
import time
from multiprocessing import Process
from signal import *
from datetime import datetime
from db import db
from flask import Flask, render_template, redirect, url_for, request
from pluginManager import pluginManager

#crons
def sync_cron():
    while True:
        print("[INFO] Starting sync cron")
        os.system("python3 r2Sync.py")  
        print("[INFO] sync cron finished")
        print("[INFO] Starting scheduler cron")
        os.system("python3 scheduler.py")  
        print("[INFO] scheduler cron finished")
        time.sleep(setting.syncCronInterval)


def killer_cron():
    while True:
        print("[INFO] Starting killer cron")
        os.system("python3 killer.py")  
        print("[INFO] killer cron finished")
        time.sleep(setting.killerCronInterval)

def startCrons():
    crons = [
        Process(target=sync_cron),
        Process(target=killer_cron)
    ]
    
    for cron in crons:
        cron.start()

    return crons

def getSatIcon(satId):
    if os.path.isfile("./static/images/satellites/%i.png" % (satId)):
        return "/static/images/satellites/%i.png" % (satId)

    return "/static/images/satellites/default.png"


app      = Flask(__name__)
plugins  = pluginManager(setting.plugins)
database = db("main")
crons    = startCrons()

@app.route('/')
def root():
    curUtc = datetime.utcnow().timestamp()
    h24s   = 86400

    return render_template(
        'home.html',
        plannedLen       = len(database.planedPassList()),
        todayLen         = len(database.observationListInTime(curUtc, h24s, 10000)),
        todayPackets     = database.sumOfDecodedPacketsInTime(curUtc, h24s),
        todayDecoded     = len(database.hasDataInTime(curUtc, h24s)),
        groundStationLen = len(setting.groundStations),
        obsSatsNum       = len(database.activeScheduleList()),
        siteName         = setting.siteName,
        bestImage        = database.bestImageInTime(curUtc, h24s),
        obs              = database.hasData(10),
        datetime         = datetime,
        sats             = database.activeSatellites(),
        getSatIcon       = getSatIcon,
        groundStations   = setting.groundStations
    )

@app.route('/observation')
def observation():
    obId        = request.args.get('ob')
    ob          = database.observation(obId)
    pluginsHtml = [""]

    plugins.onLoadObservationSite(ob, pluginsHtml)

    return render_template(
        'observation.html',
        ob = ob, 
        pluginsHtml = pluginsHtml[0],
        siteName = setting.siteName,
        path = os.path,
        datetime = datetime,
        setting = setting,
        getSatIcon = getSatIcon
    )

@app.route('/gallery')
def gallery():
    pass
    """@todo
    return render_template(
        'gallery.html',
        obs = db.galleryItemList(setting.observationsLimit, setting.galleryMinScore),
        siteName = setting.siteName
    )
    """

@app.route('/observationlist')
def observationList():
    sat  = request.args.get('sat')
    time = request.args.get('time')
    ground = request.args.get('ground')

    
    if sat != None:
        main_title   = "All observations of satellite %s" % sat
        observations = database.observationListOfSat(sat, setting.observationsLimit)
    elif time != None:
        main_title   = "All observations near %s" % time

        date = datetime.strptime(time, "%Y-%m-%d")
        timestamp = datetime.timestamp(date)

        observations = database.observationListInTime(timestamp, setting.timeRange, setting.observationsLimit)
    elif ground != None:
        main_title   = "All observations by GroundStation %s" % setting.groundStations[int(ground)]['name']

        observations =  database.planedPassListOfGroundStation(ground)
        observations += database.observationListOfGroundStation(ground, setting.observationsLimit)
    else:
        main_title   = "All observations"

        observations =  database.planedPassList()
        observations += database.observationList(setting.observationsLimit)

    return render_template(
        'observationList.html',
        obs        = observations,
        siteName   = setting.siteName,
        datetime   = datetime,
        main_title = main_title
    )