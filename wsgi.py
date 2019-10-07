#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""wsgi file
Use with gunicorn

gunicorn -w 1 --bind 0.0.0.0:14001 wsgi

"""
from shelfie_server import create_app

application = create_app() # pylint: disable=invalid-name


if __name__ == "__main__":
    application.run()
