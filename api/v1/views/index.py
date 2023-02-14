#!/usr/bin/python3

"""returns status of api"""

from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=["GET"])
def status():
    """returns status of api"""
    return jsonify({"status": "OK"})
