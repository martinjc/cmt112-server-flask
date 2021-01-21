from library import app, db
from models import *

from flask import jsonify, request


@app.route("/loans", methods=["GET"])
def get_loans():
    loans = Loan.query.all()
    ret = [l.to_json() for l in loans]
    return jsonify(ret)


@app.route("/loans/<loan_id>", methods=["GET"])
def get_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    ret = loan.to_json()
    return jsonify(ret)


@app.route("/loans/<loan_id>", methods=["PUT"])
def update_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    user = User.query.get_or_404(request.form["user"])
    book = Book.query.get_or_404(request.form["book"])
    loan.due_date = request.form["dueDate"]
    loan.user = user
    loan.book = book
    db.session.add(loan)
    db.session.commit()
    ret = loan.to_json()
    return jsonify(ret)


@app.route("/loans/<loan_id>", methods=["DELETE"])
def delete_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    db.session.delete(loan)
    db.session.commit()
    return jsonify("")
