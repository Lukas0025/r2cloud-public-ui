function createMap(id) {
    var map = L.map(id, {
        scrollWheelZoom: false
    });
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    return map;
}

function addGroundStation(map, lat, lon) {
    return L.marker([lat, lon]).addTo(map)
                               .bindPopup('GroundStation');
}

function addSatelliteTrack(map, track) {
    var polyline = L.polyline(track , {color: 'red'}).addTo(map);
    map.fitBounds(polyline.getBounds());
}

function getGroundTrackOfTle(tle, start, end) {
    var step  = 30; // in sec
    var track = [];

    var satrec = satellite.twoline2satrec(tle[0], tle[1]);

    for (var i = start; i < end; i += step) {
        var time = new Date(i * 1000);

        var positionEci = satellite.propagate(satrec, time).position;
        var gmst        = satellite.gstime(time);
        var positionGd  = satellite.eciToGeodetic(positionEci, gmst);

        track.push([
            satellite.degreesLat(positionGd.latitude),
            satellite.degreesLong(positionGd.longitude)
        ]);
    }

    return track
}

function loadTle(id) {
    return [
        document.getElementById(id).getAttribute("line2"),
        document.getElementById(id).getAttribute("line3")
    ]
}