#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""MQTT definition"""

from flask import current_app
from flask_mqtt import Mqtt

mqtt = Mqtt()


@mqtt.on_subscribe()
def handle_subscribe(*args, **kwargs):
    """Handle subscription"""
    pass


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    """Subscribe to topic on connect"""
    #mqtt.subscribe("server/update")
    pass

@mqtt.on_message()
def handle_message(client, userdata, message):
    """Handle individual messages"""
    #data = dict(topic=message.topic, payload=message.payload.decode())
    pass

@mqtt.on_publish()
def on_publish(client, userdata, mid):
    """jandle event on publishing to a topic"""
    current_app.logger.info("{}, {}, {} being published.".format(client, userdata, mid))
