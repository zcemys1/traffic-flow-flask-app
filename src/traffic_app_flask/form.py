from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from . import db
from .models import Borough


def boroughs():
    """Return a query to get the list of teams for the QuerySelectField.
    https://wtforms-sqlalchemy.readthedocs.io/en/latest/wtforms_sqlalchemy/#wtforms_sqlalchemy.fields.QuerySelectField
    """

    result = db.session.query(Borough).all()
    print("QUERY RESULT:", result)
    return result

    # borough_list = db.session.execute(db.select(Borough.borough_name)).scalars()
    # print(borough_list)
    # return borough_list


class BoroughFlowForm(FlaskForm):
    """Form for selecting borough and year for traffic flow data."""

    borough = QuerySelectField(
        "Select Borough",
        query_factory=boroughs,
        allow_blank=True,
        validators=[DataRequired()],
    )


class TrafficDataRequestForm(FlaskForm):
    """Form for requesting traffic data."""

    borough = QuerySelectField(
        "Select Borough",
        query_factory=boroughs,
        allow_blank=True,
        get_label="borough_name",
        validators=[DataRequired()],
    )
    year = SelectField(
        "Select Year",
        choices=[(str(year), str(year)) for year in range(1993, 2024)],
        validators=[DataRequired()],
    )
    # Vehicle type selection
    vehicle_type = RadioField(
        "Select Vehicle Type",
        choices=[("cars", "Cars"), ("all_vehicles", "All Vehicles")],
        validators=[DataRequired()],
    )
