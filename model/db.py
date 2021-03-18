from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from enum import Enum

db = SQLAlchemy()

class PrintJob(db.Model):
    class Status(Enum):
        NEW = 1,
        PRINTING = 2,
        FINISHED = 3,
        FAILED = 4

    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(80), unique=False, nullable=False)
    author = db.Column(db.String(80), unique=False, nullable=False)
    netid = db.Column(db.String(7), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=True)
    customer_name = db.Column(db.String(80), unique=False, nullable=True)
    length = db.Column(db.Interval, unique=False, nullable=False)
    status = db.Column(db.Enum(Status), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=True)

    def __init__(self, job_name=None, author="Makerspace", netid=None, email=None, customer_name=None, length=None, status=Status.NEW):
        super().__init__(job_name=job_name, author=author, netid=netid, email=email, customer_name=customer_name, length=length, status=status)

    def __repr__(self):
        return f"{self.id}: {self.job_name}"

class Printer(db.Model):
    class Status(Enum):
        IDLE = 1,
        PRINTING = 2,
        DOWN = 3

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    func = db.Enum(enums=["FDM, SLA"], unique=False, nullable=False)
    status = db.Column(db.Enum(Status), unique=False, nullable=False)

    def __init__(self, name, func, status=Status.IDLE):
        super().__init__(name=name, func=func, status=status)

    def __repr__(self):
        return f"{self.id}: {self.name}"