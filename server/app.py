#!/usr/bin/env python3

# Standard library imports

# Remote library imports

from flask import request, make_response, abort, jsonify, render_template, session    
from flask_restful import Resource
import os
from uuid import uuid4
from dotenv import load_dotenv
load_dotenv()

# Local imports
from config import app, db, api
from models import User

# Views go here!


@app.route('/')
@app.route('/<int:id>')
def index(id=0):
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
