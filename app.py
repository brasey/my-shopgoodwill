#!/usr/bin/env python
"""Web app to display my-shopgoodwill"""

from datetime import datetime
import os
from pytz import timezone
from flask import Flask, render_template, url_for
from firebase_admin import firestore
from db import db

app = Flask(__name__)
listings = []

@app.route("/")
def index():
    """Main page"""
    return render_template('layout.html', listings=get_listings())

def get_listings():
    """Get the listings from the database"""
    # Set end of "today" for query date range
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    end_time = datetime.strptime(f"{year}-{month}-{day} 23:59:59", "%Y-%m-%d %H:%M:%S")
    eastern = timezone('US/Eastern')
    end_time = eastern.localize(end_time)

    firebase_docs = db.collection('listings').where(
            'end_time', '>=', now
        ).where(
            'end_time', '<=', end_time
        ).order_by(
            'end_time', direction=firestore.Query.ASCENDING
        ).stream()

    listings.clear()
    for doc in firebase_docs:
        listings.append(doc.to_dict())
    return listings


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
