# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify

WHO = Blueprint('who', __name__)


@WHO.route('/', methods=['GET'])
def who():
    return jsonify(who="GAE")
