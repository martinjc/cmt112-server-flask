from library import app, db
from models import *

from flask import jsonify, request


@app.route("/loans", methods=["GET"])
def get_loans():
    loans = Loan.query.all()
    ret = [l.to_json() for l in loans]
    return jsonify(ret)


@app.route("/loans/<loan_id>", methods=["GET", "PUT", "DELETE"])
def get_loan(loan_id):
    if request.method == "GET":
        loan = Loan.query.get_or_404(loan_id)
        ret = loan.to_json()
        return jsonify(ret)
    elif request.method == "PUT":
        loan = Loan.query.get_or_404(loan_id)
        loan.due_date = datetime.fromisoformat(request.json["dueDate"])
        db.session.add(loan)
        db.session.commit()
        ret = loan.to_json()
        return jsonify(ret)
    elif request.method == "DELETE":
        loan = Loan.query.get_or_404(loan_id)
        db.session.delete(loan)
        db.session.commit()
        return jsonify("")
