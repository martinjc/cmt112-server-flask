from library import app, db
from models import *

from flask import jsonify, request


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    ret = [a.to_json() for a in users]
    return jsonify(ret)


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    ret = user.to_json()
    return jsonify(ret)


@app.route("/users/<user_id>/loans", methods=["GET"])
def get_user_loans(user_id):
    user = User.query.get_or_404(user_id)
    loans = Loan.query.filter_by(user=user)
    ret = [l.to_json() for l in loans]
    return jsonify(ret)


@app.route("/users/<user_id>/loans/<book_id>", methods=["POST"])
def get_or_make_loan(user_id, book_id):
    user = User.query.get_or_404(user_id)
    book = Book.query.get_or_404(book_id)
    loan = Loan(user=user, book=book, due_date=request.form["dueDate"])
    db.session.add(loan)
    db.session.commit()
    ret = loan.to_json()
    return jsonify(ret)


@app.route("/users", methods=["POST"])
def create_users():
    user = User(
        name=request.form["name"],
        barcode=request.form["barcode"],
        membertype=request.form["memberType"],
    )
    db.session.add(user)
    db.session.commit()
    ret = user.to_json()
    return jsonify(ret)


@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.name = request.form["title"]
    user.barcode = request.form["barcode"]
    user.membertype = request.form["memberType"]
    db.session.add(user)
    db.session.commit()
    ret = user.to_json()
    return jsonify(ret)


@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify("")

