import os
from flask import Flask
from .dash_app.dashboard import init_dash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from pathlib import Path


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # specify the location of the database, which is in the database folder and not in the instance folder
    trafficdb_location = Path(__file__).parent.joinpath("database", "traffic.db")
    app.config.from_mapping(
        SECRET_KEY="dev",
        # SQLALCHEMY_DATABASE_URI = "sqlite:///C:\\Users\\uswe\\OneDrive - University College London\\Desktop\\COMP0034 T2 2025\\comp0034-cw2-zcemys1\\src\\instance\\traffic.db",
        # SQLALCHEMY_DATABASE_URI = "sqlite:///../src/instance/traffic.db",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + str(trafficdb_location),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
    )

    if test_config is not None:
        # load the instance config, if it exists, when not testing
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    with app.app_context():

        db.create_all()
        # pass

    # import routes from starter
    from . import routes

    app.register_blueprint(routes.bp)

    init_dash(app)

    # Add the shutdown function here to clean up sessions after each request
    # @app.teardown_appcontext
    # def shutdown_session(exception=None):
    #   db.session.remove()

    return app


# flask --app src.traffic_app_flask run --debug
