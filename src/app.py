import datetime
import json
import pandas as pd
import os

from dateutil import parser as dateparser
from pushbullet import Pushbullet
from dotenv import load_dotenv
load_dotenv()

from nsapi import NSAPI

pb = Pushbullet(os.environ["API_KEY_PUSHBULLET"])
ns = NSAPI(os.environ["API_KEY_NS"])

stations = ns.get_all_stations()

trips_parsed = []


def get_station_uic(station_name):
    """
    Given a station name, return its uic, by searching in the stations list
    
    Args:
        station_name (string): Exact name of the station
    
    Returns:
        string: uic of the station
    """
    for station in stations:
        if station_name == station.names['lang']:
            return station.uic_code


def get_ns_trip(uic_start, uic_end, time_start, time_end):
    """
    Gets ns trip specification object given a route string
    """
    result = ns.get_trip(f"arnu|fromStation={uic_start}|toStation={uic_end}|plannedFromTime={time_start}|plannedArrivalTime={time_end}|yearCard=false|excludeHighSpeedTrains=false")
    return result


def parse_upcoming_trips(trips, minutes_delta):
    """
    Loops through the specified trips and if the trip is within the next minutes_delta minutes
    then the trip metadata is requested from the ns api and added to the result list
    
    Args:
        trips (list[dict]): list of the specified trips
    
    Returns:
        list: list of ns-objects of trips that are within next delta minutes
    """

    result = []
    for trip in trips:
        station_start_uic = get_station_uic(trip["station_origin"])
        station_end_uic = get_station_uic(trip["station_destination"])

        dt_start = dateparser.parse(trip["time_origin"])
        dt_arrive = dateparser.parse(trip["time_destination"])

        diff_start = (dt_start - datetime.datetime.now()).total_seconds() / 60.0
        diff_end = (dt_arrive - datetime.datetime.now()).total_seconds() / 60.0
        
        start = dt_start.strftime("%Y-%m-%dT%H:%M:%S+01:00")
        arrive = dt_arrive.strftime("%Y-%m-%dT%H:%M:%S+01:00")

        if abs(diff_start) < minutes_delta or abs(diff_end) < minutes_delta:
            trip_parsed = get_ns_trip(station_start_uic, station_end_uic, start, arrive)
            result.append(trip_parsed)

    return result

def has_delays(trip):
    """
    Checks ns-trip object and looks if there is a delay in departure and arrival times
    """
    t = trip["legs"][0]

    result = True
    if "actualDateTime" in t["origin"] and "actualDateTime" in t["destination"]:
        result = t["origin"]["plannedDateTime"] == t["origin"]["actualDateTime"] and \
                 t["destination"]["plannedDateTime"] == t["destination"]["actualDateTime"]
    
    return not result

# list of trips defined in trips.csv
trips = pd.read_csv("trips.csv").to_dict('records')
# list of the same trips but these are ns-objects
trips_parsed = parse_upcoming_trips(trips, 30)

for trip in trips_parsed:
    if has_delays(trip):
        start = trip["legs"][0]["origin"]["name"]
        end = trip["legs"][0]["destination"]["name"]

        print(f"Delay on {start} - {end}")
        pb.push_note("Delay!", f"There is a delay on the trip {start} - {end}")
