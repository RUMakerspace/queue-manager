from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PrintJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(80), unique=False, nullable=False)
    author = db.Column(db.String(80), unique=False, nullable=False)
    netid = db.Column(db.String(7), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=True)
    customer_name = db.Column(db.String(80), unique=False, nullable=True)
    length = db.Column(db.Time, unique=False, nullable=False)
    status = db.Column(db.String(10), unique=False, nullable=False)

    def __repr__(self):
        return f"{self.name}: {self.length}"