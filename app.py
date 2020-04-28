from flask import Flask, jsonify
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

conn = engine.connect()
Base=automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

app = Flask(__name__)
@app.route("/")
def home():
    return(f"Available Routes:</br>"
           f"/api/v1.0/precipitation</br>"
           f"/api/v1.0/stations</br>"
           f"/api/v1.0/tobs</br>"
           f"/api/v1.0/<start></br>"
           f"/api/v1.0/<start>/<end>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp = session.query(measurement.date, measurement.prcp).\
           filter(measurement.date >= year_ago).all()
    prcp = {date: prcp for date, prcp in prcp}
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(station.station).all()
    stations = list(np.ravel(stations))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs = session.query(measurement.tobs).filter(measurement.date >= year_ago).\
           filter(measurement.station == "USC00519281").all()
    tobs = list(np.ravel(tobs))
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def calculate_temp_start(start):
    result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start).all()
    result = list(np.ravel(result))
    return jsonify(result)

@app.route("/api/v1.0/<start>/<end>")
def calculate_temp_both(start, end):
    result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
             filter(measurement.date >= start).filter(measurement.date <= end).all()
    result = list(np.ravel(result))
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)