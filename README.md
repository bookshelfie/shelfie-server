# shelfie-server

`shelfie` is my micropython-based bookshelf inventory management program.
I wanted a way to organize my books in an easy way, and to retrieve their
positions from the bookshelf using WS2818B Addressable RGB LEDs. I also wanted
an independent method to index the bookshelf, without relying on GoodReads.

In the future, this API will be tied in with Alexa, and Telegram for a bot that
I can use to query it. I will also make a Web UI for it.

## Shelfie Flask Server

This repository contains the microservice that provides the core
functionality of `shelfie`.

## Architecture

Shelfie needs the following:

1. Mosquitto MQTT
2. Postgresql Server (can use mariadb or sqlite3, but I recommend postgres.


## Deployment

### Notes for the Raspberry Pi

I primarily deploy this on a Raspberry Pi 3B+ running Rasbian 9.9 Stretch,
so these are steps that pertain to it.

```bash
# these steps are necessary because the pip binaries in Canonical's repositories
# are outdated. The same trickles down to all debian based OSes,
# including Raspbian.
apt-get remove python-pip python3-pip
wget https://bootstrap.pypa.io/get-pip.py
# python get-pip.py # optional, if you'd like to patch pip2.
python3 get-pip.py
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### gunicorn service file

As always, run this with a gunicorn service file.

```ini
[Unit]
Description=shelfie voice gunicorn
After=network.target

[Service]
User=user
Group=group
WorkingDirectory=/home/user/shelfie-server
Environment="PATH=/home/user/shelfie-server/env/bin"
ExecStart=/home/user/shelfie-server/env/bin/gunicorn --workers 1 --bind 0.0.0.0:13001 wsgi

[Install]
WantedBy=multi-user.target

```

### nginx configuration

Load balance the gunicorn service with nginx.

```
location / {
    proxy_pass http://localhost:13001;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $remote_addr;
    port_in_redirect off;
    proxy_redirect http://localhost:13001;
}
```

## Development Notes

1. Ensure **all** routes end with `/`.
