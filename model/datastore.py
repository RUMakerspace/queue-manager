from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timezone

db = SQLAlchemy()


class Print(db.Model):
    print_pk = db.Column(db.Integer, primary_key=True)

    print_name = db.Column(db.String(40), unique=False, nullable=True)
    print_notes = db.Column(db.String(1000), unique=False, nullable=False)
    print_finished = db.Column(
        db.Boolean, nullable=False, default=False
    )  # while this _is_ a boolean, we will have a function to help with this.
    print_cost = db.Column(
        db.Numeric
    )  # numeric is a real, fixed precision number.  Handy!
    print_user_email = db.Column(db.String(100), unique=False, nullable=False)
    print_user_netid = db.Column(db.String(40), unique=False, nullable=False)
    print_user_name = db.Column(db.String(100), unique=False, nullable=False)
    print_payment_type = db.Column(
        db.String(40), unique=False, nullable=True
    )  # This should be like 'Credit', 'RUExpress, 'IPO', etc.
    print_ipo_info = db.Column(db.String(50), unique=False, nullable=True)

    def __repr__(self):
        return "<PrintJob {} {} {}".format(
            print_pk, print_name, print_notes, print_user_primary
        )


class BuildPlate(db.Model):
    buildplate_pk = db.Column(db.Integer, primary_key=True)
    print_pk = db.Column(db.Integer, db.ForeignKey("print.print_pk"), nullable=False)

    # plate setup name types and stuff.
    buildplate_type = db.Column(
        db.String(20), unique=False, nullable=False
    )  # SLA, FDM, Markforged, etc
    buildplate_material_used = db.Column(
        db.String(40), unique=False, nullable=False
    )  # PETG, FDM, Resin, etc.
    buildplate_material_color = db.Column(
        db.String(40), unique=False, nullable=False
    )  # Grey, Galaxy Purple, etc.


class PrintLog(db.Model):
    printlog_pk = db.Column(db.Integer, primary_key=True)
    print_pk = db.Column(db.Integer, db.ForeignKey("print.print_pk"), nullable=False)
    printlog_type = db.Column(
        db.String(40), unique=False, nullable=False
    )  # like 'started', 'emailed', 'picked up'
    printlog_message = db.Column(
        db.String(200), unique=False, nullable=False
    )  # like "print failed again."
    printlog_staff_name = db.Column(
        db.String(40), unique=False, nullable=False
    )  # staff name.
    printlog_time = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )


# I don't actually know the right way to enforce this at the DB level.  Damn.
