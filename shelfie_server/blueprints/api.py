#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic API"""

import json

from flask import Blueprint, request, jsonify, abort

from shelfie_server.models import db
from shelfie_server.models.book import Book

from shelfie_server.extensions.mqtt import mqtt

api = Blueprint("api", __name__)


@api.route("/book/", methods=["GET", "POST", "PUT", "DELETE"])
def manage_book():
    """Book endpoint."""
    # pylint: disable=no-member
    title = request.args.get("title")
    if request.method == "GET":
        book = Book.query.filter(Book.title.like(title)).first()
        if book:
            # write to mqtt
            response = {"book": {"title": book.title, "author": book.author}}
            if book.shelf and book.slots:
                response["shelf"] = book.shelf
                response["slot_start"] = book.slots
                mqtt.publish(f"BOOKSHELF/{book.shelf.upper()}", json.dumps(response))
            else:
                #
                message = {"color": (255, 0, 0), "blink": True, "times": 2}
                mqtt.publish(f"ALERT/PRIME", json.dumps(message))
            return jsonify(response)
        else:
            return abort(404)
    elif request.method == "PUT":
        shelf = request.args.get("shelf")
        slots = request.args.get("slots")
        book = Book.query.filter(Book.title.like(title)).first()
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
        message = {"color": (0, 255, 0), "blink": True, "times": 3}
        mqtt.publish("ALERT/PRIME", json.dumps(message))
        return jsonify(response)
    elif request.method == "DELETE":
        return abort(404)
