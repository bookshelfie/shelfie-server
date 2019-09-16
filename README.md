# shelfie-server

`shelfie` is my micropython-based bookshelf inventory management program.
I wanted a way to organize my books in an easy way, and to retrieve their
positions from the bookshelf using WS2818B Addressable RGB LEDs. I also wanted
an independent method to index the bookshelf, without relying on GoodReads.

In the future, this API will be tied in with Alexa, and Telegram for a bot that
I can use to query it. I will also make a Web UI for it.

## Shelfie Bookshelf Search Engine Flask Server

This repository contains the microservice that provides the core
functionality of `shelfie`.

## Architecture

Shelfie needs the following:

1. Mosquitto MQTT
2. Postgresql Server (can use mariadb or sqlite3, but I recommend postgres.
