from library import app, db
from models import *

from datetime import datetime
from flask import jsonify, request


@app.route("/users", methods=["GET", "POST"])
def get_users():
    if request.method == "GET":
        users = User.query.all()
        ret = [a.to_json() for a in users]
        return jsonify(ret)
    elif request.method == "POST":
        user = User(
            name=request.json["name"],
            barcode=request.json["barcode"],
            membertype=request.json["memberType"],
        )
        db.session.add(user)
        db.session.commit()
        ret = user.to_json()
        return jsonify(ret)


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    ret = user.to_json()
    return jsonify(ret)


@app.route("/users/<user_id>/loans", methods=["GET", "PUT", "DELETE"])
def get_user_loans(user_id):
    if request.method == "GET":
        user = User.query.get_or_404(user_id)
        loans = Loan.query.filter_by(user=user.id)
        ret = [l.to_json() for l in loans]
        return jsonify(ret)
    elif request.method == "PUT":
        user = User.query.get_or_404(user_id)
        user.name = request.json["title"]
        user.barcode = request.json["barcode"]
        user.membertype = request.json["memberType"]
        db.session.add(user)
        db.session.commit()
        ret = user.to_json()
        return jsonify(ret)
    elif request.method == "DELETE":
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify("")


@app.route("/users/<user_id>/loans/<book_id>", methods=["POST"])
def get_or_make_loan(user_id, book_id):
    user = User.query.get_or_404(user_id)
    book = Book.query.get_or_404(book_id)
    loan = Loan(
        user=user.id,
        book=book.id,
        due_date=datetime.fromisoformat(request.json["dueDate"]),
    )
    db.session.add(loan)
    db.session.commit()
    ret = loan.to_json()
    return jsonify(ret)

