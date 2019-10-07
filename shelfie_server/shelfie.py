#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Shelfie server application definition"""


from flask import Flask
from flask_admin.contrib.sqla import ModelView

def create_app(config=None):
    """shelfie app factory method"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.base")
    if config:
        app.config.from_object(config)
    # attempt to read a config from the instance folder.
    app.config.from_pyfile("config.py", silent=True)
    app.config.from_envvar("SHELFIE_SERVER_CONFIG", silent=True)

    from shelfie_server.models import db

    db.init_app(app)
    from shelfie_server.extensions import migrate

    migrate.init_app(app, db)

    from shelfie_server.models.book import Book # pylint: disable=unused-import

    from shelfie_server.extensions import mqtt
    mqtt.init_app(app)
    from shelfie_server.extensions import admin

    admin.init_app(app)

    class CustomView(ModelView):
        list_template = 'list.html'
        create_template = 'create.html'
        edit_template = 'edit.html'


    class BookAdmin(CustomView):
        column_searchable_list = (
            'author', 'isbn', 'title','slots','publisher','_format')
        column_filters = (
            'author', 'title', 'slots', 'publisher', '_format', 'shelf')

    admin.add_view(BookAdmin(Book, db.session))
    from shelfie_server.blueprints import api

    app.register_blueprint(api, url_prefix="/api/v1")
    return app
