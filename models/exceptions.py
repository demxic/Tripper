""" Module to catch and handle expected exceptions """


class UnsavedAirport(Exception):
    def __init__(self, airport_iata_code):
        super().__init__("Error! {} airport is not stored in the database".format(airport_iata_code))
        self.airport_iata_code = airport_iata_code


class UnsavedRoute(Exception):
    def __init__(self, route):
        super().__init__("route: {} is not stored in the data base".format(route))
        self.route = route
