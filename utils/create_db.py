from flask import Flask
from sqlalchemy import text
from models import db

def create_db(app: Flask):
    with app.app_context():
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        db.session.commit()

        db.drop_all()
        db.create_all()

        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        db.session.commit() 
