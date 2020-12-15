from library import app, db
from models import *

from flask import jsonify, request


@app.route("/authors", methods=["GET"])
def get_authors():
    authors = Author.query.all()
    entities = request.args.get("allEntities", False)
    ret = [a.to_json(entities) for a in authors]
    return jsonify(ret)


@app.route("/authors/<author_id>", methods=["GET"])
def get_author(author_id):
    author = Author.query.get_or_404(author_id)
    entities = request.args.get("allEntities", False)
    ret = author.to_json(entities)
    return jsonify(ret)


@app.route("/authors", methods=["POST"])
def create_authors():
    author = Author(name=request.form["name"])
    db.session.add(author)
    db.session.commit()
    ret = author.to_json()
    return jsonify(ret)


@app.route("/authors/<author_id>/books", methods=["POST"])
def add_book_to_author(author_id):
    author = Author.query.get_or_404(author_id)
    book = Book.query.filter_by(
        title=request.form["title"], isbn=request.form["isbn"]
    ).first()
    if book is None:
        book = Book(title=request.form["title"], isbn=request.form["isbn"])
        author.books.append(book)
        db.session.add(book)
        db.session.add(author)
        db.session.commit()
    ret = author.to_json(entities=True)
    return jsonify(ret)


@app.route("/authors/<author_id>", methods=["PUT"])
def update_author(author_id):
    author = Author.query.get_or_404(author_id)
    author.name = request.form["name"]
    db.session.add(author)
    db.session.commit()
    entities = request.args.get("allEntities", False)
    ret = author.to_json(entities)
    return jsonify(ret)


@app.route("/authors/<author_id>", methods=["DELETE"])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    return jsonify("")

