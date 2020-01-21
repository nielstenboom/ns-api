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
    for station in stations:
        if station_name == station.names['lang']:
            return station.uic_code


def get_ns_trip(uic_start, uic_end, time_start, time_end):
    result = ns.get_trip(f"arnu|fromStation={uic_start}|toStation={uic_end}|plannedFromTime={time_start}|plannedArrivalTime={time_end}|yearCard=false|excludeHighSpeedTrains=false")
    return result


def parse_upcoming_trips(trips):
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
        if abs(diff_start) < 20 or abs(diff_end) < 20:
            trip_parsed = get_ns_trip(station_start_uic, station_end_uic, start, arrive)
            result.append(trip_parsed)

    return result

def has_delays(trip):
    t = trip["legs"][0]

    result = True
    if "actualDateTime" in t["origin"] and "actualDateTime" in t["destination"]:
        result = t["origin"]["plannedDateTime"] == t["origin"]["actualDateTime"] and \
                 t["destination"]["plannedDateTime"] == t["destination"]["actualDateTime"]
    
    return not result


trips = pd.read_csv("trips.csv").to_dict('records')
trips_parsed = parse_upcoming_trips(trips)

for trip_parsed, trip in zip(trips_parsed, trips):
    if has_delays(trip_parsed):
        start = trip["station_origin"]
        end = trip["station_destination"]

        print(f"Delay on {start} - {end}")
        pb.push_note("Delay!", f"There is a delay on the trip {start} - {end}")
