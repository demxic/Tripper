"""Concrete schedule classes related classes.

All classes needed to implement a crew scheduling app

"""


class Airline(object):
    """Basic class used to model an airline"""
    _airlines = dict()

    def __new__(cls, airline_code: str, airline_name: str) -> "Airline":
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