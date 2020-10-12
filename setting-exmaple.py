#from plugins import plugin1 plugin2

siteName           = "r2Cloud public UI"

enableAPI          = True
APILimit           = 100

galleryMinScore    = 0.70
galletySats        = ["METEOR-M 2"]

observationsLimit  = 200

observationTTL     = 0  # in days 0 means never die
rawsTTL            = 5  # in days 0 means never die
aTTL               = 0  # in days 0 means never die
spectrogramsTTL    = 10 # in days 0 means never die
dataTTL            = 0  # in days 0 means never die

timeRange          = 86400 # in timestrap (sec)

syncA              = True
syncSpectrograms   = True
syncRaws           = True
syncData           = True

syncCronInterval   = 3600  #in sec
killerCronInterval = 86400 #in sec

#plugins = [plugin1, plugin2]
plugins = []

groundStations    = [
    {
        "id"   : 0,
        "lon"  : 16.5735250,
        "lat"  : 40.2406544,
        "alt"  : 200, 
        "name" : "22DBKB",
        "addr" : "https://10.0.0.99",
        "user" : "test@test",
        "pass" : "mypassword",
        "img"  : "static/user/R0P01.jpg",
        "short_about": "Station located in ...."
    },

    {
        "id"   : 1,
        "lon"  : 16.5735250,
        "lat"  : 0.2406544,
        "alt"  : 0, 
        "name" : "my sea station",
        "addr" : "https://10.0.0.100",
        "user" : "test@test",
        "pass" : "mypassword",
        "img"  : "static/user/sea.jpg",
        "short_about": "Station located in ...."
    }
]