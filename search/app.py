#!/usr/bin/python3
"""Instantiate a Flask application"""

from flask import jsonify, request, abort, make_response, Flask, render_template
from search_aggregate.bing_engine import bing
from search_aggregate.google_engine import google
from search_aggregate.wiki import wiki

#create flask instance and register search_views blueprint on it to manage
qalchemy = Flask(__name__)


@qalchemy.route("/", strict_slashes=False)
def index():
    """render qalchemy's frontend page -- nginx will handle this later"""
    return render_template("index.html")


@qalchemy.route("/search", methods=["POST"], strict_slashes=False)
def search():
    """generate search result"""
    if request.method == "POST":
        query = request.get_json().get("q")
        if query:
            wiki_r = wiki(query)
            w = [{"title": "sorry No relevant search result from wikipedia"}]
            if wiki_r and len(wiki_r) != 0:
                w = wiki_r
            google_r  = google(query)
            bing_r = bing(query)
            return jsonify([{"engine": "Google", "results": google_r}, {"engine": "Bing", "results": bing_r}, {"engine": "Wiki", "results": w}])
    return "Enter search input" #this message should probably be flash to user


@qalchemy.errorhandler(404)
def handler_error(err):
    """handle error 404"""
    return make_response(jsonify([{"error": "bad query"}]), 404)


if __name__ == "__main__":
    """launch qalchemy"""
    qalchemy.run(host="0.0.0.0", port=5000, threaded=True)
