from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

db = SQLAlchemy()

class PrintJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(80), unique=False, nullable=False)
    author = db.Column(db.String(80), unique=False, nullable=False)
    netid = db.Column(db.String(7), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=True)
    customer_name = db.Column(db.String(80), unique=False, nullable=True)
    length = db.Column(db.Interval, unique=False, nullable=False)
    status = db.Column(db.String(10), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=True)

    # Test
    def __init__(self, job_name=None, author="Makerspace", netid=None, email=None, customer_name=None, length=None, status="NEW"):
        super().__init__(job_name=job_name, author=author, netid=netid, email=email, customer_name=customer_name, length=length, status=status)

    def __repr__(self):
        return f"{self.id}: {self.job_name}"
