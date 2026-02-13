from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from . import db


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]


class Borough(db.Model):
    __tablename__ = "boroughs"
    borough_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    la_code: Mapped[str] = mapped_column(String(10), nullable=False)
    borough_name: Mapped[str] = mapped_column(String(50), nullable=False)

    def __str__(self):
        return self.borough_name


class TrafficFlow(db.Model):
    __tablename__ = "traffic_flows"
    flow_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    borough_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("boroughs.borough_id")
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    cars: Mapped[float] = mapped_column(db.Float, nullable=False)
    all_vehicles: Mapped[float] = mapped_column(db.Float, nullable=False)


borough = db.relationship("Borough", backref=db.backref("traffic_flows", lazy=True))
