#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic API"""

import json

from flask import Blueprint, request, jsonify, abort, current_app

from shelfie_server.models import db
from shelfie_server.models.book import Book

from shelfie_server.extensions.mqtt import mqtt

api = Blueprint("api", __name__) # pylint: disable=invalid-name


@api.route("/alert/<shelf>/")
def alert(shelf=None):
    """Alert System
    Expected keys in request.data:
        blink: boolean
        kind: string,
        times: int, default=2
    """

    message = {
        "kind": request.data.get("kind", "info"),
        "blink": request.data.get("blink", True),
        "times": request.data.get("times", 2)
    }
    if shelf is None:
        for shelf_lbl in current_app.config["SHELF_LABELS"]:
            mqtt.publish("shelfie/alert/{}".format(shelf_lbl.lower()), json.dumps(message))
    else:
        mqtt.publish("shelfie/alert/{}".format(shelf.lower()), json.dumps(message))
    response = {"success.lower()": True}
    return jsonify(response)


@api.route("/progress/<shelf>/")
def show_progress(shelf=None):
    """Show progress bar.
    Expected Keys:
        progress: float

    Writes to shelfie/progress/{shelf}
    """
    progress = request.data.get("progress", 0)
    message = {
        "progress": float(progress)
    }
    if shelf is None:
        for shelf_lbl in current_app.config["SHELF_LABELS"]:
            # does it make sense to send the progress to all the shelves?
            mqtt.publish("shelfie/progress/{}".format(shelf_lbl.lower()), json.dumps(message))
    else:
        mqtt.publish("shelfie/progress/{}".format(shelf.lower()), json.dumps(message))
    response = {"success": True}
    return jsonify(response)


@api.route("/highlight/<shelf>/")
def highlight(shelf=None):
    """Highlight nth LEDs so that it is easy to index.
    Expected Keys:
        n: int, default=10

        Writes to shelfie/highlight/{shelf}
    """
    message = {"steps": request.data.get("steps", 10 )}
    if shelf is None:
        for shelf_lbl in current_app.config["SHELF_LABELS"]:
            mqtt.publish("shelfie/highlight/{}".format(shelf_lbl.lower()), json.dumps(message))
    else:
        mqtt.publish("shelfie/highlight/{}".format(shelf.lower()), json.dumps(message))
    response = {"success": True} # FIXME: What point does this serve?
    return jsonify(response)


@api.route("/clear/<shelf>/")
def clear(shelf=None):
    """Route that clears all LEDs for one or all shelves."""
    if shelf is None:
        for shelf_lbl in current_app.config["SHELF_LABELS"]:
            mqtt.publish("shelfie/clear/{}".format(shelf_lbl.lower()), "")
    else:
        mqtt.publish("shelfie/clear/{}".format(shelf.lower()), "")
    response = {"success": True}
    return jsonify(response)


@api.route("/book/", methods=["GET", "POST", "PUT", "DELETE"])
def manage_book():
    """Book endpoint."""
    # pylint: disable=no-member
    title = request.args.get("title")
    if request.method == "GET":
        if title is None:
            return abort(400)
        current_app.logger.info("Searching for a book named `{}`".format(title))
        book = Book.query.filter(Book.title.ilike("%{}%".format(title))).first()
        if book:
            current_app.logger.info("Book found: {}".format(book.title))
            # write to mqtt
            response = {
                "book":
                {
                    "title": book.title,
                    "author": book.author
                }
            }
            if book.shelf and book.slots:
                # response["shelf"] = book.shelf
                response["positions"] = book.slots
                mqtt.publish("shelfie/{}".format(book.shelf.lower()), json.dumps(response))
            else:
                message = {"color": (255, 0, 0), "blink": True, "times": 2}
                mqtt.publish("shelfie/alert", json.dumps(message))
            return jsonify(response)
        else:
            current_app.logger.warning("no match for '{}'".format(title))
            return abort(404)
    elif request.method == "PUT":
        title = request.args.get("title")
        shelf = request.args.get("shelf")
        slots = request.args.get("slots")
        book = Book.query.filter(Book.title.ilike("%{}%".format(title))).first()
        if book:
            if shelf and slots:
                book.shelf = shelf
                book.slots = slots
                db.session.commit()
            else:
                return abort(400)
        else:
            return abort(404)
    elif request.method == "POST":
        title = request.args.get("title")
        isbn = request.args.get("isbn")
        author = request.args.get("author")
        publisher = request.args.get("publisher")
        width = request.args.get("width")
        height = request.args.get("height")
        shelf = request.args.get("shelf")
        slots = request.args.get("slots")
        book = Book(title=title, author=author)
        if isbn:
            book.isbn = isbn
        if width:
            book.width = float(width)
        if height:
            book.height = float(height)
        if shelf:
            book.shelf = shelf
        if slots:
            book.slots = slots
        if publisher:
            book.publisher = publisher
        db.session.add(book)
        db.session.commit()
        response = {"success": True}
        message = {"color": (0, 255, 128), "blink": True, "times": 3}
        for shelf_lbl in current_app.config["SHELF_LABELS"]:
            mqtt.publish("alert/{}".format(shelf_lbl.lower()), json.dumps(message))
        return jsonify(response)
    else: # if request.method == "DELETE":
        return abort(404)
