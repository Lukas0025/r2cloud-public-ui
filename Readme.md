# r2cloud-public-ui
Unofficial website ui for r2clouds servers. Designed to display your recorded data to the public. It accesses the date via the API and allows data to be collected from multiple stations

## Setup using docker
* create own setting file (`setting.py`), exemple you can found in `setting-exmaple.py`
* run docker container with command 

```sh
docker run -d \
  --name=r2cloud-public-ui \
  -mount type=bind,source="$(pwd)/setting.py",target="/r2cloud_public_ui/setting.py" \
  -p 5000:5000 \
  lukasplevac/r2cloud-public-ui
```

### Advence docker

####  volumes
* `/r2cloud_public_ui/setting.py:ro          `- setting file
* `/r2cloud_public_ui/plugins:rw             `- dir for plugins
* `/r2cloud_public_ui/static/a:rw            `- dir with downloaded a
* `/r2cloud_public_ui/static/raws:rw         `- dir with downloaded raws
* `/r2cloud_public_ui/static/bins:rw         `- dir with downloaded binary files (decoded binary)
* `/r2cloud_public_ui/static/spectrograms:rw `- dir with downloaded spectrograms
* `/r2cloud_public_ui/static/user:ro         `- dir with user static (images of groundStations, ...)

#### ports
* `5000` - http ui website

## Setup without docker
* install `python3` and `python3-pip` - `apt install python3 python3-pip`
* from `pip3` install `r2cloud`, `Flask` and `requests` - `pip3 install Flask && pip3 install r2cloud && pip3 install requests`
* create own setting file (`setting.py`), exemple you can found in `setting-exmaple.py`
* run app using `env FLASK_APP=root.py flask run`
