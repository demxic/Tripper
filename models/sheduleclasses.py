"""Concrete schedule classes related classes.

All classes needed to implement a crew scheduling app

"""
import pytz


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

    def __new__(cls, iata_code: str = None, timezone=None, viaticum=None):
        airport = cls._airports.get(iata_code)
        if not airport:
            airport = super().__new__(cls)
            if timezone:
                cls._airports[iata_code] = airport
        return airport

    def __init__(self, iata_code: str, timezone: pytz.timezone = None, viaticum: str = None):
        """
        Represents an airport as a 3 letter code
        """
        if not hasattr(self, 'initted'):
            self.iata_code = iata_code
            self.timezone = timezone
            self.viaticum = viaticum
            self.initted = True

    def __str__(self):
        return "{}".format(self.iata_code)

    def __repr__(self):
        return "<{__class__.__name__}> {iata_code}".format(__class__=self.__class__, **self.__dict__)
