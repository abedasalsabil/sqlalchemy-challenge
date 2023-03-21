# Import the dependencies.
import numpy as np

import sqlalchemy
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#save references to each table
Measurement = Base.classes.measurement
Station=Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    
    """Return the precipitation data for last year"""
    #Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    #Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
        
    session.close()
    #Dict with date as the key and prcp as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
        

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    """Return the list of stations from the dataset"""
    # query all stations
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    
    session.close()
    
    # Convert list of tuples into normal list
    stations_list = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        station_list.append(station_dict)
        
        station_list.append(station_dict)
        
    return jsonify(station_list)
    
    
@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    #Calculate the date 1 year ago from last date in database
    """Return a list of all temperatures in the past year"""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    temp = session.query(Measurement.date, Measurement.tobs).filter_by(station = 'USC00519281').filter(Measurement.date >= prev_year).all()
    
    session.close()
    
    # Convert list of tuples into normal list
    past_12_months = []
    for date, tobs in temp:
        tobs_dict = {}
        tobs_dict[date] = tobs
        past_12_months.append(tobs_dict)
        
    return jsonify(past_12_months)
    

@app.route("/api/v1.0/temp/start")
def start():
    
    sessions= Session(engine)
    
    """Return a list of the minimum, average and maximum temperatures for the start"""
    
    temperatures = [Measurement.station,
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)]
            
    temp_query = session.query(*temperatures).filter_by(Measurement.date > start).all()
    Start_list =[{"TMIN": Query[0][1]},
                {"TAVG": Query[0][2]},
                {"TMAX": Query[0][3]}]
                
    session.close()
    

@app.route("/api/v1.0/temp/start/end")
def end():
    session = Session(engine)
    
    """Return a list of the minimum, average and maximum temperatures for the start-end"""
    temperatures = [Measurement.station,
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)]
            
    temp_query = session.query(*temperatures).filter_by(Measurement.date > end).all()
    End_list =[{"TMIN": Query[0][1]},
                {"TAVG": Query[0][2]},
                {"TMAX": Query[0][3]}]
                
    session.close()
    
    if __name__ == '__main__':
        app.run(debug=True)
