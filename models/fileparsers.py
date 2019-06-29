"""This module holds functions needed to read pbs.txt files and turn them into schedule classes"""
from models.regularexpressions import trips_total_RE, trip_RE, dutyday_RE, flights_RE
from typing import List, Dict


def number_of_trips_in_pbs_file(pbs_file_content: str) -> int:
    """Searches for the 'Total number of trips' inside the pbs_file_content and returns the total number """
    match_obj = trips_total_RE.search(pbs_file_content)
    total_trips = int(match_obj.groupdict()['trips_total'])
    return total_trips


def create_trips_as_dict(trips_as_strings: str, crew_position: str, trip_base: str) -> list:
    """Return a list containing all trip_as_dict from its corresponding trip_string"""

    dict_trips = []
    for trip_match in trip_RE.finditer(trips_as_strings):
        trip_as_dict = get_trip_as_dict(trip_match.groupdict())
        trip_as_dict['crew_position'] = crew_position
        trip_as_dict['trip_base'] = trip_base
        dict_trips.append(trip_as_dict)
        # print("Trip {} dated {} found!".format(trip_as_dict['number'], trip_as_dict['dated']))

    return dict_trips


def get_trip_as_dict(trip_dict: dict) -> dict:
    """
    Given a dictionary containing PBS trip data, turn it into a dictionary

    """
    trip_dict['date_and_time'] = trip_dict['dated'] + trip_dict['check_in']
    dds = list()

    for duty_day_match in dutyday_RE.finditer(trip_dict['duty_days']):
        duty_day = get_dutyday_as_dict(duty_day_match.groupdict())
        dds.append(duty_day)
    trip_dict['duty_days'] = dds

    return trip_dict


def get_dutyday_as_dict(duty_day_dict: dict) -> dict:
    """
    Given a dictionary containing pbs duty_day data, do some needed formatting
    """

    duty_day_dict['layover_duration'] = duty_day_dict['layover_duration'] if duty_day_dict[
        'layover_duration'] else '0000'

    # The last flight in a duty_day must be re-arranged
    dictionary_flights: List[Dict[str, str]] = [f.groupdict() for f in flights_RE.finditer(duty_day_dict['flights'])]
    duty_day_dict['rls'] = dictionary_flights[-1]['blk']
    dictionary_flights[-1]['blk'] = dictionary_flights[-1]['turn']
    dictionary_flights[-1]['turn'] = '0000'

    duty_day_dict['flights'] = dictionary_flights

    return duty_day_dict
