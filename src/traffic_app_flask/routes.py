from flask import Blueprint, render_template, request
from .form import BoroughFlowForm, TrafficDataRequestForm
from .models import TrafficFlow, Borough
import pandas as pd

# from src.traffic_app_flask import db wasnt letting tests pass
# from traffic_app_flask import db wasnt letting flask run
from . import db  # this then worked for both


bp = Blueprint("bp", __name__)


@bp.route("/")
def index():
    return render_template("index.html", message="Hello, Flask!")


# This is for dash app


@bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", dash_url="/dash_app/")


# This is for the ulez check page


@bp.route("/ulez_check/", methods=["GET", "POST"])
def ulez_check():
    result = None

    if request.method == "POST":
        fuel_type = request.form.get("fuel_type")
        year = int(request.form.get("year"))

        if fuel_type == "Petrol" and year <= 2005:
            result = "Your vehicle is NOT ULEZ compliant."
        elif fuel_type == "Diesel" and year <= 2014:
            result = "Your vehicle is NOT ULEZ compliant."
        else:
            result = "Your vehicle is ULEZ compliant."

    return render_template("ulezcheck.html", result=result)


# THIS IS FOR TRAFFIC FLOW VIEWING FORM
@bp.route("/flow/", methods=["GET", "POST"])
def flow():
    form = BoroughFlowForm()
    traffic_data = None
    historic_result = None
    borough = None
    try:
        # latest results:
        if form.validate_on_submit():
            borough = form.borough.data

            traffic_data = (
                TrafficFlow.query.filter_by(borough_id=borough.borough_id)
                .order_by(TrafficFlow.year.desc())
                .first()
            )

        # second form:
        elif request.method == "POST" and "historic_submit" in request.form:
            year = int(request.form.get("year"))
            vehicle_type = request.form.get("vehicle_type")
            borough_id_str = request.form.get("borough_id")
            if borough_id_str:
                borough_id = int(borough_id_str)
            else:
                borough_id = None

            borough = db.session.get(Borough, borough_id)

            # borough = Borough.query.get(borough_id)
            record = TrafficFlow.query.filter_by(
                borough_id=borough_id, year=year
            ).first()

            historic_result = {
                "year": year,
                "vehicle_type": vehicle_type,
                "value": getattr(record, vehicle_type) if record else None,
            }

            traffic_data = (
                TrafficFlow.query.filter_by(borough_id=borough_id)
                .order_by(TrafficFlow.year.desc())
                .first()
            )

        return render_template(
            "boroughtraffic.html",
            form=form,
            borough=borough,
            traffic_data=traffic_data,
            historic_result=historic_result,
        )
    finally:
        # Close the session to avoid any potential issues
        db.session.close()


# this is for traffic data request page


@bp.route("/data_request/", methods=["GET", "POST"])
def data_request():
    form = TrafficDataRequestForm()

    if form.validate_on_submit():
        borough_id = form.borough.data
        year = form.year.data

        borough_id = borough_id.borough_id

        # Query traffic data based on the selected borough_id and year
        traffic_data = TrafficFlow.query.filter_by(
            borough_id=borough_id, year=year
        ).all()
        print("++++++++++", traffic_data[0].borough_id)

        write_data = []
        for data in traffic_data:
            temp = {
                "year": data.year,
                "borough_name": Borough.query.get(data.borough_id).borough_name,
                "cars": data.cars,
                "all_vehicles": data.all_vehicles,
            }
            write_data.append(temp)
        print("write_data:", write_data)

        data_save = pd.DataFrame(write_data)
        data_save.to_csv("traffic_data.csv", index=False)

    # NAME THE FILE ON THE COURSEWORK THE EXPORT ONE SO SARAH DOESNT GET CONFUSED
    # # Create a CSV file from the traffic data using BytesIO
    # output = StringIO()
    # writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # # Write the header row
    # writer.writerow(['Borough', 'Year', 'Vehicle Type', 'Traffic Flow'])

    # for record in traffic_data:
    #     borough_name = record.borough_id  # Get the borough name
    #     # Normalize vehicle_type to match database column names
    #     vehicle_type_column = vehicle_type.lower()
    #     writer.writerow([borough_name, record.year, vehicle_type, getattr(record, vehicle_type_column, "N/A")])

    # # Send the CSV file as an attachment
    # return send_file(output, mimetype='text/csv', download_name='traffic_data.csv', as_attachment=True)

    return render_template("data_request.html", form=form)
