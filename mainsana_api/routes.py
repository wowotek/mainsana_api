from .engine import app
from .engine import db
from .models import *
from flask_json import json_response, request

@app.route("/register", methods=["POST"])
def register():
    for i in User.query.all():
        if i.username == request.form.get("username"):
            return json_response(
                data={
                    "msg": "username exist !",
                    "registered": False
                },
                status=400
            )

        if i.email == request.form.get("email"):
            return json_response(
                data={
                    "msg": "email exist !",
                    "registered": False
                },
                status=400
            )
        
        if i.phone = request.form.get("phone"):
            return json_response(
                data={
                    "msg": "phone number exist !",
                    "registered": False
                }
            )
    
    try:
        db.session.add(
            User(
                username=request.form.get("username"),
                password=request.form.get("password"),
                email=request.form.get("email"),
                phone=request.form.get("phone")
            )
        )
        db.session.commit()

        for i in User.query.all():
            if i.username == request.form.get("username"):
                return json_response(
                    data={
                        "msg": "registered successfully",
                        "registered": True
                    },
                    status=201
                )

        return json_response(
                data={
                    "msg": "cannot register for unknown reason !",
                    "registered": False
                },
                status=400
            )
    except Exception() as e:
        return json_response(
                data={
                    "msg": f"unknown error, {e}",
                    "registered": False
                },
                status=400
            )

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    for i in User.query.all():
        if i.username == username and i.password == password:
            return json_response(
                data={
                    "msg": "Logged In !",
                    "user": {
                        "username": i.username,
                        "email": i.email,
                        "phone": i.phone
                    },
                    "logged": True
                },
                status=200
            )

    return json_response(
        data={
            "msg": "Username / Password not registered",
            "logged": False
        },
        status=400
    )

@app.route("/add_tour")
def add_tour():
    username = request.form.get("username")

    for i in User.query.all():
        if i.username == username:
            Tour(
                user=i,
                name=request.form.get("tour_name"),
                description=request.form.get("tour_desc")
            )
    
    return json_response(
        data={
            "msg": "failed to add, username doesn't exist",
            "tour_added": False
        }