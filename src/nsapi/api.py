from typing import Dict, List, Union

import requests
import asyncio
import aiohttp

from .models import Arrival, Departure, Disruption, Station, Trip, PriceOption

class NSBase():
    base_url = 'https://gateway.apiportal.ns.nl/public-'

    @classmethod
    def _route(cls, product: str, *args) -> str:
        remainder = '/'+'/'.join(args)
        return f'{cls.base_url}{product}{remainder}'

    @staticmethod
    def _convert(payload: Union[List, Dict], model: type):
        if isinstance(payload, list):
            items = []
            for data in payload:
                item = model.from_dict(data)
                items.append(item)
            return items
        return model.from_dict(payload)

class NSAPI(NSBase):
    """
    Nederlandse Spoorwegen (NS) API.
    Wrapper to query the Public-Travel-Information API.
    """

    def __init__(self, key: str):
        self.session = requests.Session()
        self.headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Accept': 'application/json'
        }

    def _request(self, url: str, params: dict = None) -> object:
        with self.session.get(url, headers=self.headers, params=params) as request:
            request.raise_for_status()
            return request.json()

    def get_all_stations(self) -> List[Station]:
        """ List of stations """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v2/stations
        response = self._request(self._route('reisinformatie', 'api', 'v2', 'stations'))
        return self._convert(response['payload'], model = Station)

    def get_arrivals(self, **params) -> List[Arrival]:
        """ Arrival times for a specified station. Either the UIC code or station is required """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v2/arrivals[?dateTime][&maxJourneys][&lang][&station][&uicCode][&source]
        response = self._request(self._route('reisinformatie', 'api', 'v2', 'arrivals'), params = params)
        return self._convert(response['payload']['arrivals'], model = Arrival)

    def get_departures(self, **params) -> List[Departure]:
        """ Departure times for a specified station. Either the UIC code or station is required """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v2/departures[?dateTime][&maxJourneys][&lang][&station][&uicCode][&source]
        response = self._request(self._route('reisinformatie', 'api', 'v2', 'departures'), params = params)
        return response['payload']['departures']

    def get_disruption(self, id: str) -> Disruption:
        """ Specific disruption/maintenance """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v2/disruptions/{id}
        response = self._request(self._route('reisinformatie', 'api', 'v2', 'disruptions', id))
        return self._convert(response['payload'],  model = Disruption)

    def get_disruptions(self, **params) -> List[Disruption]:
        """ List of disruptions/maintenance. """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v2/disruptions[?type][&actual][&lang]
        response = self._request(self._route('reisinformatie', 'api', 'v2', 'disruptions'), params = params)
        return self._convert(response['payload'], model = Disruption)

    def get_station_disruptions(self, code: str) -> List[Disruption]:
        """ Disruptions for a station, code is either a UIC code or old-skool station code """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v2/disruptions/station/{code}
        response = self._request(self._route('reisinformatie', 'v2', 'disruptions', 'station', code))
        return self._convert(response['payload'], model = Disruption)

    def get_trip(self, ctx_recon: str, **params) -> Trip:
        """ Reconstruct a trip if possible using the given reconCtx (representation of a trip found in a travel advice) """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v3/trips/trip?ctxRecon={ctxRecon}[&date][&lang][&product][&travelClass][&discount][&travelRequestType]
        response = self._request(self._route('reisinformatie', 'api', 'v3', 'trips', 'trip'), params = {'ctxRecon': ctx_recon, **params})
        return response

    def get_trips(self, **params) -> List[Trip]:
        """ Searches for a travel advice with the specified options between the possible backends (HARP, 9292 or PAS/AVG) """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v3/trips[?originLat][&originLng][&destinationLat][&destinationLng][&viaLat][&viaLng][&viaWaitTime][&dateTime][&searchForArrival][&previousAdvices][&nextAdvices][&context][&addChangeTime][&lang][&polylines][&fromZip][&toZip][&travelMethodFrom][&travelMethodTo][&product][&travelClass][&discount][&productStationFrom][&productStationTo][&yearCard][&originTransit][&originWalk][&originBike][&originCar][&originName][&travelAssistanceTransferTime][&searchForAccessibleTrip][&destinationTransit][&destinationWalk][&destinationBike][&destinationCar][&destinationName][&accessibilityEquipment1][&accessibilityEquipment2][&excludeHighSpeedTrains][&excludeReservationRequired][&passing][&travelRequestType][&originEVACode][&destinationEVACode][&viaEVACode][&shorterChange][&fromStation][&toStation][&originUicCode][&destinationUicCode][&viaUicCode][&bikeCarriageRequired][&viaStation][&departure][&minimalChangeTime]
        response = self._request(self._route('reisinformatie', 'api', 'v3', 'trips'), params = params)
        return response['trips']

    def get_trip_price(self, from_station: str, to_station: str,**params) -> List[PriceOption]:
        """ Returns a list of price options for the requested trip."""
        # https://gateway.apiportal.ns.nl/public-prijsinformatie/prices[?date][&fromStation][&toStation]
        response = self._request(self._route('prijsinformatie', 'prices'), params = {'fromStation': from_station, 'toStation': to_station, **params})
        return self._convert(response['priceOptions'], model = PriceOption)


class AsyncNSAPI(NSBase):
    """
    Nederlandse Spoorwegen (NS) API.
    Wrapper to query the Public-Travel-Information API.
    """

    def __init__(self, key: str):
        self.headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Accept': 'application/json'
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args):
        await self.session.close()

    async def _request(self, url: str, params: dict = None) -> object:
        async with self.session.get(url, headers=self.headers, params=params) as request:
            response = await request.json()
            request.raise_for_status()
            return response

    async def get_all_stations(self) -> List[Station]:
        """ List of stations """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v2/stations
        response = await self._request(self._route('reisinformatie', 'api', 'v2', 'stations'))
        return self._convert(response['payload'], model = Station)

    async def get_arrivals(self, **params) -> List[Arrival]:
        """ Arrival times for a specified station. Either the UIC code or station is required """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v2/arrivals[?dateTime][&maxJourneys][&lang][&station][&uicCode][&source]
        response = await self._request(self._route('reisinformatie', 'api', 'v2', 'arrivals'), params = params)
        return self._convert(response['payload']['arrivals'], model = Arrival)

    async def get_departures(self, **params) -> List[Departure]:
        """ Departure times for a specified station. Either the UIC code or station is required """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v2/departures[?dateTime][&maxJourneys][&lang][&station][&uicCode][&source]
        response = await self._request(self._route('reisinformatie', 'api', 'v2', 'departures'), params = params)
        return self._convert(response['payload']['departures'],  model = Departure)

    async def get_disruption(self, id: str) -> Disruption:
        """ Specific disruption/maintenance """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v2/disruptions/{id}
        response = await self._request(self._route('reisinformatie', 'api', 'v2', 'disruptions', id))
        return self._convert(response['payload'],  model = Disruption)

    async def get_disruptions(self, **params) -> List[Disruption]:
        """ List of disruptions/maintenance. """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v2/disruptions[?type][&actual][&lang]
        response = await self._request(self._route('reisinformatie', 'api', 'v2', 'disruptions'), params = params)
        return self._convert(response['payload'], model = Disruption)

    async def get_station_disruptions(self, code: str) -> List[Disruption]:
        """ Disruptions for a station, code is either a UIC code or old-skool station code """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v2/disruptions/station/{code}
        response = await self._request(self._route('reisinformatie', 'api', 'v2', 'disruptions', 'station', code))
        return self._convert(response['payload'], model = Disruption)

    async def get_trip(self, ctx_recon: str, **params) -> Trip:
        """ Reconstruct a trip if possible using the given reconCtx (representation of a trip found in a travel advice) """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v3/trips/trip?ctxRecon={ctxRecon}[&date][&lang][&product][&travelClass][&discount][&travelRequestType]
        response = await self._request(self._route('reisinformatie', 'api', 'v3', 'trips', 'trip'), params = {'ctxRecon': ctx_recon, **params})
        return self._convert(response['payload'], model = Trip)

    async def get_trips(self, **params) -> List[Trip]:
        """ Searches for a travel advice with the specified options between the possible backends (HARP, 9292 or PAS/AVG) """
        # https://gateway.apiportal.ns.nl/public-reisinformatie/api/v3/trips[?originLat][&originLng][&destinationLat][&destinationLng][&viaLat][&viaLng][&viaWaitTime][&dateTime][&searchForArrival][&previousAdvices][&nextAdvices][&context][&addChangeTime][&lang][&polylines][&fromZip][&toZip][&travelMethodFrom][&travelMethodTo][&product][&travelClass][&discount][&productStationFrom][&productStationTo][&yearCard][&originTransit][&originWalk][&originBike][&originCar][&originName][&travelAssistanceTransferTime][&searchForAccessibleTrip][&destinationTransit][&destinationWalk][&destinationBike][&destinationCar][&destinationName][&accessibilityEquipment1][&accessibilityEquipment2][&excludeHighSpeedTrains][&excludeReservationRequired][&passing][&travelRequestType][&originEVACode][&destinationEVACode][&viaEVACode][&shorterChange][&fromStation][&toStation][&originUicCode][&destinationUicCode][&viaUicCode][&bikeCarriageRequired][&viaStation][&departure][&minimalChangeTime]
        response = await self._request(self._route('reisinformatie', 'api', 'v3', 'trips'), params = params)
        return self._convert(response['trips'], model = Trip)

    async def get_trip_price(self, from_station: str, to_station: str,**params) -> List[PriceOption]:
        """ Returns a list of price options for the requested trip."""
        # https://gateway.apiportal.ns.nl/public-prijsinformatie/prices[?date][&fromStation][&toStation]
        response = await self._request(self._route('prijsinformatie', 'prices'), params = {'fromStation': from_station, 'toStation': to_station, **params})
        return self._convert(response['priceOptions'], model = PriceOption)