#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""flask admin"""
from flask_admin import Admin

admin = Admin(
    name="shelfie",
    base_template="layout.html",
    template_mode="bootstrap3")
