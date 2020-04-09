from .engine import app
from .engine import db
from .models import *
from flask_json import json_response, request

@app.route("/register", methods=["POST"])
def register():
    for i in User.query.all():
        if i.username == request.form.get("username"):
            return json_response(
                msg="username exist !",
                status=400
            )

        if i.email == request.form.get("email"):
            return json_response(
                msg="email exist !",
                status=400
            )
        
        if i.phone == request.form.get("phone"):
            return json_response(
                msg="phone number exist !",
                status=400
            )
    
    try:
        user = User(
            username=request.form.get("username"),
            password=request.form.get("password"),
            email=request.form.get("email"),
            phone=request.form.get("phone")
        )
        db.session.add(
            user
        )
        db.session.commit()
        db.session.refresh(user)
        return json_response(
            msg="registered successfully",
            status=201
        )
    except Exception as e:
        return json_response(
                msg=f"unknown error, {e}",
                status=500
            )

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    for i in User.query.all():
        if i.username == username and i.password == password:
            return json_response(
                msg="Logged In !",
                user={
                    "id": i.id,
                    "username": i.username,
                    "email": i.email,
                    "phone": i.phone
                },
                status=200
            )

    return json_response(
        msg="Username / Password not registered",
        user={},
        status=400
    )

# TOUR #
@app.route("/add_tour", methods=["POST"])
def add_tour():
    name=request.form.get("tour_name")
    description=request.form.get("tour_desc")
    for i in User.query.all():
        if i.username == request.form.get("username"):
            try:
                t = Tour(
                    user_id=i.id,
                    name=name,
                    description=description
                )
                db.session.add(t)
                db.session.commit()

                return json_response(
                    msg=f"successfully added tour for user: {t.user.username}",
                    tour={
                        "id": t.id,
                        "user_id": t.user.id,
                        "name": t.name,
                        "desc": t.description
                    },
                    status=201
                )

            except Exception as e:
                return json_response(
                    msg=f"failed to add tour, {e}",
                    tour={},
                    status=500
                )
    
    return json_response(
        msg="failed to add, username doesn't exist",
        tour={},
        status=500
    )

@app.route("/edit_tour", methods=["POST"])
def edit_tour():
    target_id = request.form.get("tour_id")
    new_name = request.form.get("tour_name")
    new_description = request.form.get("tour_desc")

    for i in Tour.query.all():
        if str(i.id) == str(target_id):
            try:
                i.name = new_name
                i.description = new_description

                db.session.commit()

                return json_response(
                    msg=f"successfully edited tour id: {i.id}",
                    tour={
                        "id": i.id,
                        "user_id": i.id,
                        "name": i.name,
                        "desc": i.description
                    },
                    status=201
                )
            except Exception as e:
                return json_response(
                    msg=f"failed to edit tour, {e}",
                    tour={},
                    status=500
                )

    return json_response(
            msg=f"failed to edit tour, id not found",
            tour={},
            status=400
        )

@app.route("/delete_tour", methods=["POST"])
def delete_tour():
    target_id = request.form.get("tour_id")
    for i in Tour.query.all():
        if str(i.id) == str(target_id):
            try:
                db.session.delete(i)
                db.session.commit()
                return json_response(
                    msg=f"success deleted tour : {target_id}",
                    tour={},
                    status=201
                )
            except Exception as e:
                return json_response(
                    msg=f"failed to delete tour, {e}",
                    tour={},
                    status=500
                )

    return json_response(
            msg=f"failed to delete tour, id not found",
            tour={},
            status=400
        )

# TRIP #
@app.route("/add_trip", methods=["POST"])
def add_trip():
    for i in Tour.query.all():
        if str(i.id) == str(request.form.get("tour_id")):
            try:
                trip = Trip(
                    tour = i,
                    name = request.form.get("trip_name"),
                    description = request.form.get("trip_desc")
                )
                db.session.add(
                    trip
                )
                db.session.commit()
                return json_response(
                    msg=f"success added trip, for user: {i.user.username}, tour: {i.name} | {i.id}",
                    trip={
                        "id": trip.id,
                        "tour_id": i.id,
                        "name": trip.name,
                        "desc": trip.description
                    },
                    status=200
                )
            except Exception as e:
                return json_response(
                    msg=f"failed to add trip, {e}",
                    trip={},
                    status=500
                )

    return json_response(
            msg=f"failed to add trip, Tour not found",
            trip={},
            status=400
        )

@app.route("/edit_trip", methods=["POST"])
def edit_trip():
    target_id = request.form.get("trip_id")
    new_name = request.form.get("trip_name")
    new_description = request.form.get("trip_desc")

    for i in Trip.query.all():
        print(i.id)
        if str(i.id) == str(target_id):
            try:
                i.name = new_name
                i.description = new_description

                db.session.commit()
                return json_response(
                    msg=f"success edited trip, tour: {i.tour.name} | {i.id}",
                    trip={
                        "id": i.id,
                        "tour_id": i.tour.id,
                        "name": i.name,
                        "desc": i.description
                    },
                    status=200
                )
            except Exception as e:
                return json_response(
                    msg=f"failed to edit trip, {e}",
                    trip={},
                    status=500
                )

    return json_response(
            msg=f"failed to edit trip, id not found",
            trip={},
            status=400
        )


@app.route("/delete_trip", methods=["POST"])
def delete_trip():
    target_id = request.form.get("trip_id")
    for i in Trip.query.all():
        if str(i.id) == str(target_id):
            try:
                db.session.delete(i)
                db.session.commit()
                return json_response(
                    msg=f"success deleted trip : {target_id}",
                    trip={},
                    status=201
                )
            except Exception as e:
                return json_response(
                    msg=f"failed to delete trip, {e}",
                    trip={},
                    status=500
                )

    return json_response(
            msg=f"failed to delete trip, id not found",
            trip={},
            status=400
        )

# BUDGETS #
@app.route("/add_budget", methods=["POST"])
def add_budget():
    for i in Trip.query.all():
        if str(i.id) == str(request.form.get("trip_id")):
            try:
                budget = Budget(
                    trip=i,
                    name=request.form.get("budget_name"),
                    description=request.form.get("budget_desc"),
                    budget=float(request.form.get("budget_budget")),
                    budget_type_id=int(request.form.get("budget_type_id"))
                )
                db.session.add(budget)
                db.session.commit()
                return json_response(
                    msg=f"success added budget for trip: {i.name}",
                    budget={
                        "id": budget.id,
                        "trip_id": i.id,
                        "name": budget.name,
                        "desc": budget.description,
                        "amount": float(budget.budget),
                        "budget_type_id": budget.budget_type.name
                    },
                    status=201
                )
            except Exception as e:
                return json_response(
                    msg=f"failed to add budget, {e}",
                    budget={},
                    status=500
                )

    return json_response(
            msg=f"failed to add budget, id not found",
            budget={},
            status=400
        )

@app.route("/edit_budget", methods=["POST"])
def edit_budget():
    target_id = request.form.get("budget_id")
    new_name = request.form.get("budget_name")
    new_description = request.form.get("budget_desc")
    new_budget = float(request.form.get("budget_budget"))
    new_budget_type_id = int(request.form.get("budget_type_id"))
    for i in Budget.query.all():
        if str(i.id) == str(target_id):
            try:
                i.name = new_name
                i.description = new_description
                i.budget = float(new_budget)
                i.budget_type_id = int(new_budget_type_id)

                db.session.commit()
                return json_response(
                    msg=f"success edited budget : {i.id}",
                    budget={
                        "id": i.id,
                        "trip_id": i.trip.id,
                        "name": i.name,
                        "desc": i.description,
                        "amount": float(i.budget),
                        "budget_type_id": i.budget_type.name
                    },
                    status=201
                )
            except Exception as e:
                return json_response(
                    msg=f"failed to edit budget, {e}",
                    budget={},
                    status=500
                )

    return json_response(
            msg=f"failed to edit budget, id not found",
            budget={},
            status=400
        )

@app.route("/delete_budget", methods=["POST"])
def delete_budget():
    target_id = request.form.get("budget_id")
    for i in Budget.query.all():
        if str(i.id) == str(target_id):
            try:
                db.session.delete(i)
                db.session.commit()
                return json_response(
                    msg=f"success deleted budget : {target_id}",
                    budget={},
                    status=201
                )
            except Exception as e:
                return json_response(
                    msg=f"failed to delete budget, {e}",
                    budget={},
                    status=500
                )

    return json_response(
            msg=f"failed to delete budget, id not found",
            budget={},
            status=400
        )