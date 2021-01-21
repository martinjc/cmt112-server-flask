from library import db
from models import *
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


if __name__ == "__main__":
    db.create_all()
    book1 = Book(title="How to Draw Good", isbn="3289589036")
    book2 = Book(title="Making the Cake", isbn="23567035")
    book3 = Book(title="Laughing for No Reason", isbn="3297806")
    author1 = Author(name="Arthur James")
    author2 = Author(name="Evelyn Dorothy")
    author3 = Author(name="Lisa Jones")
    book1.authors.append(author1)
    book2.authors.append(author3)
    book3.authors.append(author2)
    book3.authors.append(author1)
    user1 = User(name="Martin Chorley", barcode="123456", membertype="Staff")
    db.session.add(book1)
    db.session.add(book2)
    db.session.add(book3)
    db.session.add(author1)
    db.session.add(author2)
    db.session.add(author3)
    db.session.add(user1)
    db.session.commit()
    loan = Loan(
        due_date=datetime.fromisoformat("2020-05-06"), book=book1.id, user=user1.id
    )
    db.session.add(loan)
    db.session.commit()
