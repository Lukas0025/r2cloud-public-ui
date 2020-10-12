FROM debian:buster
MAINTAINER Lukas Plevac

RUN apt-get update && \
    apt-get -y upgrade && DEBIAN_FRONTEND=noninteractive apt-get -y install \
    python3 python3-pip && \
    pip3 install Flask && \
    pip3 install r2cloud

#add system
ADD src/. /r2cloud_public_ui

EXPOSE 5000
VOLUME ["/r2cloud_public_ui/setting.py", "/r2cloud_public_ui/plugins", "/r2cloud_public_ui/static/a", "/r2cloud_public_ui/static/bins", "/r2cloud_public_ui/static/plugins", "/r2cloud_public_ui/static/user", "/r2cloud_public_ui/static/raws", "/r2cloud_public_ui/static/spectrograms"]
CMD ["cd", "/r2cloud_public_ui", "&&", "env", "FLASK_APP=root.py", "flask run"]