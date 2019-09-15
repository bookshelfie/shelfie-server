#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Shelfie server application definition"""


from flask import Flask


def create_app(config=None):
    """shelfie app factory method"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.base")
    if config:
        app.config.from_object(config)
    app.config.from_pyfile("config.py", silent=True)
    app.config.from_envvar("SHELFIE_SERVER_CONFIG", silent=True)

    from shelfie_server.models import db

    db.init_app(app)
    from shelfie_server.extensions import migrate

    migrate.init_app(app, db)

    from shelfie_server.models.book import Book # pylint: disable=unused-import

    from shelfie_server.extensions import mqtt

    mqtt.init_app(app)
    from shelfie_server.blueprints import api

    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(api, url_prefix="/api/v1")
    return app
