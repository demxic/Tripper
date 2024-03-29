"""This module stores the classes need to turn pbs-dictionaries into schedule objects. """
import pytz

from models.exceptions import UnsavedAirport, UnsavedRoute
from models.sheduleclasses import Airport, Route


class ScheduleObjectBuilder(object):
    """This class takes a dictionary or a string and turns them into corresponding
        schedule objects
    """

    def __init__(self, crew_position: str, trip_base: str):
        self.crew_position = crew_position
        self.trip_base = Airport.load_from_db(airport_iata_code=trip_base)

    @staticmethod
    def build_timezone(zone: str):
        return pytz.timezone(zone=zone)

    def build_airport(self, airport_iata_code: str) -> Airport:
        try:
            stored_airport = Airport.load_from_db(airport_iata_code=airport_iata_code)
        except UnsavedAirport as e:
            print(e)
            ans = input("Want to save it Y/N ? ").capitalize()
            if ans == 'Y':
                zone = input("Enter timezone ")
                print("Choose a viaticum zone "
                      "paris, new_york, usa, low_cost, "
                      "madrid, high_cost, border")
                viaticum_zone = input()
                unstored_airport = Airport(airport_iata_code=airport_iata_code,
                                           timezone=self.build_timezone(zone=zone),
                                           viaticum=viaticum_zone)
                stored_airport = unstored_airport.save_to_db()
            else:
                raise e
        return stored_airport

    def build_route(self, event_name: str, origin: Airport, destination: Airport) -> Route:
        # route = Route(event_name=event_name, origin=origin, destination=destination)
        # if not route.route_id:
        route = None
        try:
            route = Route.load_from_db(event_name=event_name, origin=origin, destination=destination)
        except UnsavedRoute as e:
            print(e)
            ans = input("Want to save it Y/N? ").capitalize()
            if ans == 'Y':
                e.route.save_to_db()
                route = e.route
            else:
                raise e
        return route
