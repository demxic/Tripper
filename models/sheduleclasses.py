"""Concrete schedule classes related classes.

All classes needed to implement a crew scheduling app

"""
import pytz
from data.database import CursorFromConnectionPool
from models.exceptions import UnsavedAirport, UnsavedRoute


class Airline(object):
    """Basic class used to model an airline"""
    _airlines = dict()

    def __new__(cls, airline_code: str, airline_name: str) -> 'Airline':
        airline = cls._airlines.get(airline_code)
        if not airline:
            airline = super().__new__(cls)
            cls._airlines[airline_code] = airline
        return airline

    def __init__(self, airline_code: str, airline_name: str = "Aeroméxico"):
        if not hasattr(self, 'initted'):
            self.airline_code = airline_code
            self.airline_name = airline_name
            self.initted = True

    def __str__(self):
        return self.airline_code if self.airline_code else 2 * ' '

    def __repr__(self):
        return "<{__class__.__name__}> {airline_code}".format(__class__=self.__class__, **self.__dict__)


class Airport(object):
    """Create airports using the Flyweight pattern
    Try using the weakref.WeakValueDictionary() if  garbage-collection concerned
    for our simple app, not needed
    """
    _airports = dict()

    def __new__(cls, airport_iata_code: str = None, timezone=None, viaticum=None):
        airport = cls._airports.get(airport_iata_code)
        if not airport:
            airport = super().__new__(cls)
            if timezone:
                cls._airports[airport_iata_code] = airport
        return airport

    def __init__(self, airport_iata_code: str, timezone: pytz.timezone = None, viaticum: str = None):
        """
        Represents an airport as a 3 letter code
        """
        if not hasattr(self, 'initted'):
            self.airport_iata_code = airport_iata_code
            self.timezone = timezone
            self.viaticum = viaticum
            self.initted = True

    @classmethod
    def load_from_db(cls, airport_iata_code: str):
        airport = cls._airports.get(airport_iata_code.upper())
        if not airport:
            with CursorFromConnectionPool() as cursor:
                cursor.execute('SELECT * FROM airports WHERE iata_code=%s;', (airport_iata_code,))
                airport_data = cursor.fetchone()
            if airport_data:
                timezone = pytz.timezone(airport_data[1] + '/' + airport_data[2])
                airport = cls(airport_iata_code=airport_data[0], timezone=timezone, viaticum=airport_data[3])
            else:
                raise UnsavedAirport(airport_iata_code=airport_iata_code)
        return airport

    def save_to_db(self):
        continent, tz_city = self.timezone.zone.split('/')
        with CursorFromConnectionPool() as cursor:
            cursor.execute('INSERT INTO public.airports(iata_code, continent, tz_city, viaticum_zone) '
                           'VALUES (%s, %s, %s, %s) '
                           'RETURNING iata_code; ',
                           (self.airport_iata_code, continent, tz_city, self.viaticum))
            iata_code = cursor.fetchone()[0]
        return iata_code

    def __str__(self):
        return "{}".format(self.airport_iata_code)

    def __repr__(self):
        return "<{__class__.__name__}> {airport_iata_code}".format(__class__=self.__class__, **self.__dict__)


class Equipment(object):
    _equipments = dict()

    def __new__(cls, airplane_code, cabin_members):
        """Use the flyweight pattern to create only one object """
        equipment = cls._equipments.get(airplane_code)
        if not equipment:
            equipment = super().__new__(cls)
            cls._equipments[airplane_code] = equipment
        return equipment

    def __init__(self, airplane_code: str, cabin_members: int = 0):
        if not hasattr(self, 'initted'):
            self.airplane_code = airplane_code
            self.cabin_members = cabin_members
            self.initted = True

    def __str__(self):
        return self.airplane_code if self.airplane_code else 3 * ' '

    def __eq__(self, other) -> bool:
        return self.airplane_code == other.airplane_code

    def __repr__(self):
        return "<{__class__.__name__}> {airplane_code}".format(__class__=self.__class__, **self.__dict__)


class Route(object):
    """For a given airline, represents a flight number or ground duty name
        with its origin and destination airports
        Note: flights and ground duties are called Events"""
    _routes = dict()

    def __new__(cls, event_name: str, origin: Airport, destination: Airport, route_id: int = None):
        route_key = event_name + origin.airport_iata_code + destination.airport_iata_code
        route = cls._routes.get(route_key)
        if not route:
            route = super().__new__(cls)
            if route_id:
                cls._routes[route_key] = route
        return route

    def __init__(self, event_name: str, origin: Airport, destination: Airport, route_id: int = None):
        """Flight numbers have 4 digits only"""
        if not hasattr(self, 'initted'):
            self.route_id = route_id
            self.event_name = event_name
            self.origin = origin
            self.destination = destination
            self.initted = True

    @classmethod
    def load_from_db(cls, event_name: str, origin: Airport, destination: Airport) -> 'Route':
        route_key = event_name + origin.airport_iata_code + destination.airport_iata_code
        loaded_route = cls._routes.get(route_key)
        if not loaded_route or not loaded_route.route_id:
            with CursorFromConnectionPool() as cursor:
                cursor.execute('SELECT route_id FROM public.routes '
                               '    WHERE event_name=%s'
                               '      AND origin=%s'
                               '      AND destination=%s',
                               (event_name, origin.airport_iata_code, destination.airport_iata_code))
                route_id = cursor.fetchone()
            if route_id:
                loaded_route = cls(event_name=event_name, origin=origin, destination=destination,
                                   route_id=route_id[0])
            else:
                raise UnsavedRoute(route=cls(event_name=event_name, origin=origin, destination=destination))
        return loaded_route

    def save_to_db(self):
        with CursorFromConnectionPool() as cursor:
            cursor.execute('INSERT INTO public.routes(event_name, origin, destination) '
                           'VALUES (%s, %s, %s) '
                           'RETURNING route_id; ',
                           (self.event_name, self.origin.airport_iata_code, self.destination.airport_iata_code))
            route_id = cursor.fetchone()[0]
            self.route_id = route_id
        return route_id

    def __eq__(self, other):
        """Two routes are the same if their parameters are equal"""
        return all((self.event_name == other.event_name, self.origin == other.origin,
                    self.destination == other.destination))

    def __str__(self):
        return "{event_name} {origin} {destination}".format(**self.__dict__)

    def __repr__(self):
        return "<{__class__.__name__}> {event_name} {origin} {destination}".format(
            __class__=self.__class__, **self.__dict__)
