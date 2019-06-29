from data.database import Database
from models.fileparsers import number_of_trips_in_pbs_file, create_trips_as_dict
from models.objectbuilders import ScheduleObjectBuilder

data_folder = "C:/Users/demxi/Google Drive/Sobrecargo/PBS/2019 PBS/201905 PBS/"
file_name = "201905 - PBS vuelos EJE.txt"
crew_position = 'EJE'
trip_base = 'MEX'
Database.initialise(database="tripper", user="Xico", password="semiconductor",
                    host="tripper.cpccqvkq54qu.us-east-2.rds.amazonaws.com")


with open(data_folder + file_name, 'r') as file:
    content = file.read()
total_trips_in_pbs_file = number_of_trips_in_pbs_file(content)
trips_as_dict = create_trips_as_dict(pbs_trips=content)
builder = ScheduleObjectBuilder(crew_position=crew_position, trip_base=trip_base)
builder.build_airport('MEX')
builder.build_airport('SCL')
builder.build_airport('AAG')