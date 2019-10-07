#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""wsgi file
Use with gunicorn

gunicorn -w 1 --bind 0.0.0.0:14001 wsgi

"""
from shelfie_server import create_app


if __name__ == "__main__":
    app = create_app() # pylint: disable=invalid-name
    app.run()
else:
    import logging
    application = create_app() # pylint: disable=invalid-name
    gunicorn_logger = logging.getLogger("gunicorn.error")
    application.logger.handlers = gunicorn_logger.handlers
    application.logger.setLevel(gunicorn_logger.level)
