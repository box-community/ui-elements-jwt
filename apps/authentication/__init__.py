# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present [Box](https://developer.box.com/)
"""

from flask import Blueprint

blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix=''
)
