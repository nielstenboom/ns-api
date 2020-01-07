from dataclasses import dataclass, field
from dataclasses_json import LetterCase, dataclass_json, config
from typing import Any, Dict, List, Optional, Union

@dataclass_json
@dataclass
class Station:
    eva_code: str = field(metadata=config(field_name='EVACode'))
    code: str
    uic_code: str = field(metadata=config(field_name='UICCode'))
    stationtype:  str = field(metadata=config(field_name='stationType'))
    names: Dict[str, str] = field(metadata=config(field_name='namen'))
    country: str = field(metadata=config(field_name='land'))
    latitude: float = field(metadata=config(field_name='lat'))
    longitude: float = field(metadata=config(field_name='lng'))
    radius: int
    approach_radius: int = field(metadata=config(field_name='naderenRadius'))
    has_facilities: bool = field(metadata=config(field_name='heeftFaciliteiten'))
    has_tavelassistance: bool = field(metadata=config(field_name='heeftReisassistentie'))
    has_departure_times: bool = field(metadata=config(field_name='heeftVertrektijden'))
    synonyms: List[str] = field(metadata=config(field_name='synoniemen'))
    tracks: Optional[List[Dict[str, str]]] = field(default=None, metadata=config(field_name='sporen'))


@dataclass_json
@dataclass
class Product:
    number: str
    category_code: str = field(metadata=config(field_name='categoryCode'))
    short_category_name: str = field(metadata=config(field_name='shortCategoryName'))
    long_category_name: str = field(metadata=config(field_name='longCategoryName'))
    operator_code: str = field(metadata=config(field_name='operatorCode'))
    operator_name: str = field(metadata=config(field_name='operatorName'))
    product_type: str = field(metadata=config(field_name='type'))
    display_name: str = field(default=None, metadata=config(field_name='displayName'))

@dataclass_json
@dataclass
class Message:
    message: str
    style: str


@dataclass_json
@dataclass
class Arrival:
    origin: str
    name: str
    planned_track: str = field(metadata=config(field_name='plannedTrack'))
    actual_track: str = field(metadata=config(field_name='actualTrack'))
    product: Product
    train_category: str = field(metadata=config(field_name='trainCategory'))
    cancelled: bool
    planned_datetime: str = field(metadata=config(field_name='plannedDateTime'))
    planned_timezone_offset: str = field(metadata=config(field_name='plannedTimeZoneOffset'))
    actual_datetime: str = field(metadata=config(field_name='actualDateTime'))
    actual_timezone_offset: str = field(metadata=config(field_name='actualTimeZoneOffset'))
    messages: Optional[List[Message]] = None


@dataclass_json
@dataclass
class Departure:
    direction: str
    name: str
    planned_datetime: str = field(metadata=config(field_name='plannedDateTime'))
    planned_timezone_offset: str = field(metadata=config(field_name='plannedTimeZoneOffset'))
    actual_datetime: str = field(metadata=config(field_name='actualDateTime'))
    actual_timezone_offset: str = field(metadata=config(field_name='actualTimeZoneOffset'))
    planned_track: str = field(metadata=config(field_name='plannedTrack'))
    actual_track: str = field(metadata=config(field_name='actualTrack'))
    product: Product
    train_category: str = field(metadata=config(field_name='trainCategory'))
    cancelled: bool
    route_stations: List[Dict[str, str]] = field(metadata=config(field_name='routeStations'))
    departure_status: str = field(metadata=config(field_name='departureStatus'))
    messages: Optional[List[Message]] = None

@dataclass_json
@dataclass
class Report:
    id: str
    type: str
    title: str = field(metadata=config(field_name='titel'))
    description: str = field(metadata=config(field_name='beschrijving'))
    last_update: str = field(metadata=config(field_name='laatstGewijzigd'))


@dataclass_json
@dataclass
class TravelAdvice:
    title: str = field(metadata=config(field_name='titel'))
    advice: List[Dict[str, str]] = field(metadata=config(field_name='reisadvies'))


@dataclass_json
@dataclass
class DisruptionTracks:
    stations: List[str]
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    direction: Optional[str] = None


@dataclass_json
@dataclass
class DisruptionDetails:
    expectation: Optional[str] = field(default=None, metadata=config(field_name='verwachting'))
    fase: Optional[str] = None
    faseLabel: Optional[str] = None
    delay: Optional[str] = field(default=None, metadata=config(field_name='extraReistijd'))
    travel_advice: Optional[TravelAdvice] = field(default=None, metadata=config(field_name='reisadviezen'))
    alternative_travel_advice: Optional[str] = field(default=None, metadata=config(field_name='alternatiefVervoer'))
    consequence: Optional[str] = field(default=None, metadata=config(field_name='gevolg'))
    impact: Optional[int] = None
    society: Optional[int] = None
    domestic: Optional[bool] = field(default=None, metadata=config(field_name='landelijk'))
    cause: Optional[str] = field(default=None, metadata=config(field_name='oorzaak'))
    header: Optional[str] = field(default=None, metadata=config(field_name='header'))
    time: Optional[str] = field(default=None, metadata=config(field_name='meldtijd'))
    duration: Optional[str] = field(default=None, metadata=config(field_name='periode'))
    traject: Optional[List[DisruptionTracks]] = field(default=None, metadata=config(field_name='baanvakken'))
    tracks: Optional[List[DisruptionTracks]] = field(default=None, metadata=config(field_name='trajecten'))
    version: Optional[str] = field(default=None, metadata=config(field_name='versie'))
    reference_number: Optional[str] = field(default=None, metadata=config(field_name='volgnummer'))
    priority: Optional[int] = field(default=None, metadata=config(field_name='prioriteit'))


@dataclass_json
@dataclass
class Disruption:
    id: str
    type: str
    title: str = field(metadata=config(field_name='titel'))
    topic: Optional[str] = None
    report: Optional[Report] = field(default=None, metadata=config(field_name='melding'))
    details: Optional[DisruptionDetails] = field(default=None, metadata=config(field_name='verstoring'))

@dataclass_json
@dataclass
class Link:
    params: Optional[str] = None
    title: Optional[str] = None
    rel: Optional[str] = None
    rels: Optional[List[str]] = None
    uri: Optional[str] = None
    type: Optional[str] = None

@dataclass_json
@dataclass
class Note:
    value: str
    key: str
    note_type: Optional[str] = field(default=None, metadata=config(field_name='noteType'))
    priority: Optional[int] = None
    route_index_from: Optional[int] = field(default=None, metadata=config(field_name='routeIdxFrom'))
    route_index_to: Optional[int] = field(default=None, metadata=config(field_name='routeIdxTo'))
    link: Optional[Link] = None
    alternative_transport: Optional[bool] = field(default=None, metadata=config(field_name='alternativeTransport'))
    is_presentation_required: Optional[bool] = field(default=None, metadata=config(field_name='isPresentationRequired'))

@dataclass_json
@dataclass
class TripOriginDestination:
    name: Optional[str] = None
    latitude: Optional[float] = field(default=None, metadata=config(field_name='lat'))
    longitude: Optional[float] = field(default=None, metadata=config(field_name='lng'))
    country_code: Optional[str] = field(default=None, metadata=config(field_name='countryCode'))
    uic_code: Optional[str] = field(default=None, metadata=config(field_name='uicCode'))
    weight: Optional[int] = None
    products: Optional[int] = None
    type: Optional[str] = None
    prognosis_type: Optional[str] = field(default=None, metadata=config(field_name='prognosisType'))
    planned_timezone_offset: Optional[int] = field(default=None, metadata=config(field_name='plannedTimeZoneOffset'))
    planned_datetime: Optional[str] = field(default=None, metadata=config(field_name='plannedDateTime'))
    actual_timezone_offset: Optional[int] = field(default=None, metadata=config(field_name='actualTimeZoneOffset'))
    actual_datetime: Optional[str] = field(default=None, metadata=config(field_name='actualDateTime'))
    planned_track: Optional[str] = field(default=None, metadata=config(field_name='plannedTrack'))
    checkin_status: Optional[str] = field(default=None, metadata=config(field_name='checkinStatus'))
    actual_track: Optional[str] = field(default=None, metadata=config(field_name='actualTrack'))
    city: Optional[str] = None
    exit_side: Optional[str] = None
    travel_assistence_meeting_points: Optional[List[str]] = field(default=None, metadata=config(field_name='travelAssistanceMeetingPoints'))
    notes: Optional[List[Note]] = None
    domestic: Optional[bool] = None
    latest_known_track: Optional[str] = field(default=None, metadata=config(field_name='latestKnownTrack'))
    # travelAssistanceBookingInfo: 


@dataclass_json
@dataclass
class LegStop:
    index: Optional[int] = field(default=None, metadata=config(field_name='routeIdx'))
    prognosis_type: Optional[str] = field(default=None, metadata=config(field_name='departurePrognosisType'))
    cancelled: Optional[bool] = None
    name: Optional[str] = None
    uic_code: Optional[str] = field(default=None, metadata=config(field_name='uicCode'))
    country_code: Optional[str] = field(default=None, metadata=config(field_name='countryCode'))
    latitude: Optional[float] = field(default=None, metadata=config(field_name='lat'))
    longitude: Optional[float] = field(default=None, metadata=config(field_name='lng'))
    planned_departure_timezone_offset: Optional[int] = field(default=None, metadata=config(field_name='plannedDepartureTimeZoneOffset'))
    planned_departure_datetime: Optional[str] = field(default=None, metadata=config(field_name='plannedDepartureDateTime'))
    planned_departure_track: Optional[str] = field(default=None, metadata=config(field_name='plannedDepartureTrack'))
    planned_arrival_timezone_offset: Optional[int] = field(default=None, metadata=config(field_name='plannedArrivalTimeZoneOffset'))
    planned_arrival_datetime: Optional[str] = field(default=None, metadata=config(field_name='plannedArrivalDateTime'))
    planned_arrival_track: Optional[str] = field(default=None, metadata=config(field_name='plannedArrivalTrack'))
    actual_arrival_timezone_offset: Optional[int] = field(default=None, metadata=config(field_name='actualArrivalTimeZoneOffset'))
    actual_arrival_datetime: Optional[str] = field(default=None, metadata=config(field_name='actualArrivalDateTime'))
    actual_arrival_track: Optional[str] = field(default=None, metadata=config(field_name='actualArrivalTrack'))
    departure_delay: Optional[int] = field(default=None, metadata=config(field_name='departureDelayInSeconds'))
    arrival_delay: Optional[int] = field(default=None, metadata=config(field_name='arrivalDelayInSeconds'))
    passing: Optional[bool] = None

@dataclass_json
@dataclass
class JourneyDetail:
    type: str
    link: Dict[str, str]



@dataclass_json
@dataclass
class Leg:
    origin: TripOriginDestination
    destination: TripOriginDestination
    index: Optional[str] = field(default=None, metadata=config(field_name='idx'))
    name: Optional[str] = None
    travel_type: Optional[str] = field(default=None, metadata=config(field_name='travelType'))
    cancelled: Optional[bool] = None
    change_possible: Optional[bool] = field(default=None, metadata=config(field_name='changePossible'))
    alternative_transpant: Optional[bool] = field(default=None, metadata=config(field_name='alternativeTransport'))
    journey_detail_ref: Optional[str] = field(default=None, metadata=config(field_name='journeyDetailRef'))
    product: Optional[Product] = None
    notes: Optional[List[Note]] = None
    stops: Optional[List[LegStop]] = None
    steps: Optional[List[Any]] = None
    shorter_stock: Optional[bool] = field(default=None, metadata=config(field_name='shorterStock'))
    journey_detail: Optional[List[JourneyDetail]] = field(default=None, metadata=config(field_name='journeyDetail'))
    reachable: Optional[bool] = None
    messages: Optional[List[Message]] = None

@dataclass_json
@dataclass
class TripFare:
    price: int =  field(metadata=config(field_name='priceInCents'))
    product: str = field(metadata=config(field_name='product'))
    travel_class: str = field(metadata=config(field_name='travelClass'))
    discount: str =  field(metadata=config(field_name='discountType'))

@dataclass_json
@dataclass
class TripProductFare(TripFare):
    price_excluding_supplement: int =  field(metadata=config(field_name='priceInCentsExcludingSupplement'))

@dataclass_json
@dataclass
class TripFareOptions:
    is_international: bool =  field(metadata=config(field_name='isInternationalBookable'))
    is_international_bookable: bool =  field(metadata=config(field_name='isInternational'))
    is_eticket_buyable: bool =  field(metadata=config(field_name='isEticketBuyable'))
    is_possible_with_ovchipcard: bool =  field(metadata=config(field_name='isPossibleWithOvChipkaart'))

@dataclass_json
@dataclass
class Trip:
    planned_duration: Optional[int] = field(default=None, metadata=config(field_name='plannedDurationInMinutes'))
    transfers: Optional[int] = None
    status: Optional[str] = None
    legs: Optional[List[Leg]] = None
    # overview_polyline: List[Any]
    ctx_recon: Optional[str] = field(default=None, metadata=config(field_name='ctxRecon'))
    checksum: Optional[str] = None
    crowd_forecast: Optional[str] = None
    ctxRecon: Optional[str] = None
    actual_duration: Optional[int] = None
    index: Optional[int] = field(default=None, metadata=config(field_name='idx'))
    optimal: Optional[bool] = None
    fares: Optional[List[TripFare]] = None
    product_fare: Optional[TripFare] = None
    type: Optional[str] = None
    realtime: Optional[bool] = None
    route_id: Optional[str] = None
    share_url: Optional[Link] = None

@dataclass_json
@dataclass
class Price:
    price: int
    class_type: Optional[str] = field(default = None, metadata=config(field_name='classType'))
    discount_type: Optional[str] = field(default = None, metadata=config(field_name='discountType'))
    product_type: Optional[str] = field(default = None, metadata=config(field_name='productType'))
    supplements: Optional[Dict[str, int]] = None

@dataclass_json
@dataclass
class PriceOption:
    type: Optional[str] = None
    price_unit: Optional[int] = field(default = None, metadata=config(field_name='tariefEenheiden'))
    prices: Optional[List[Price]] = None
    total_prices: Optional[List[Price]] = field(default = None, metadata=config(field_name='totalPrices'))
    transporter: Optional[str] = None
    from_station: Optional[str] = field(default = None, metadata=config(field_name='from'))
    to_station: Optional[str] = field(default = None, metadata=config(field_name='to'))


# note type
# "UNKNOWN",
# "ATTRIBUTE",
# "INFOTEXT",
# "REALTIME",
# "TICKET",
# "HINT"

# Checkin status
# "CHECKIN",
# "CHECKOUT",
# "OVERCHECK",
# "DETOUR",
# "REQUIRED_CHECK_OUT_IN",
# "NOTHING"

# product enum
# "TRAIN",
# "BUS",
# "TRAM",
# "METRO",
# "FERRY",
# "WALK",
# "BIKE",
# "CAR",
# "TAXI",
# "SUBWAY",
# "UNKNOWN"

# message type enum
# "MAINTENANCE",
# "DISRUPTION"

# crowd forecast
# "UNKNOWN",
# "LOW",
# "MEDIUM",
# "HIGH"

# price types
# "FIXED_PRICE"
# "ROUTE_WITH_INDICATION"
# "FREE_TRAVEL"
# "ROUTE_WITHOUT_OPTIONS"

# class types
# "FIRST"
# "SECOND

# discount type
# "FORTY_PERCENT"
# "TWENTY_PERCENT"
# "FIP_LL"
# "NONE"

# price product type
# "SINGLE_FARE"
# "RETURN_FARE"
# "SINGLE_FARE_PAPER_TICKET"
# "RETURN_FARE_PAPER_TICKET"
# "SINGLE_FARE_SINGLE_USE_OV_CHIPKAART"
# "RETURN_FARE_SINGLE_USE_OV_CHIPKAART"
# "TRAJECTVRIJ_NSBUSINESSKAART"
# "TRAJECTVRIJ_JAAR"
# "TRAJECTVRIJ_MAAND"
# "RAILRUNNER"
# "SUPPLEMENT_SINGLE_USE_OV_CHIPKAART"
# "SUPPLEMENT_ICE_INTERNATIONAL"
# "SUPPLEMENT_INTERCITY_DIRECT"