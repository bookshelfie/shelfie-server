#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Book definition"""

import datetime

from shelfie_server.models.db import db


class Book(db.Model):
    """Book object definition
    Version one of the database simply lists the books in positions
    on the shelves.
    """

    __tablename__ = "books"
    # pylint: disable=no-member
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(25), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    # TODO: move author(s) to external table.
    series = db.Column(db.String(255))
    author = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(255), nullable=True)
    # TODO: add genre
    _format = db.Column("format", db.String(255), default="Paperback")
    width = db.Column(db.Float, default=1.0)
    height = db.Column(db.Float, default=1.0)
    # shelves go from A to Z
    shelf = db.Column(db.String(10), nullable=True)
    # a slot entry will be in the m:n format.
    slots = db.Column(db.String(10), nullable=True)
    placement = db.Column(db.String(25), default="vertical") # horizontal or vertical
    sold = db.Column(db.BOOLEAN, default=False)
    comment = db.Column(db.TEXT)
    created_on = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    updated_at = db.Column(db.TIMESTAMP, onupdate=datetime.datetime.now)
