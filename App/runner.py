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
mex = builder.build_airport('MEX')
mad = builder.build_airport('MAD')
lhr = builder.build_airport('LHR')
scl = builder.build_airport('SCL')
cdg = builder.build_airport('CDG')
r1 = builder.build_route('0001', mex, mad)
print("{} is stored in DB with route_id: {}".format(r1, r1.route_id))
r2 = builder.build_route('0002', mad, mex)
print("{} is stored in DB with route_id: {}".format(r2, r2.route_id))
r1 = builder.build_route('0001', mex, mad)
print("{} is stored in DB with route_id: {}".format(r1, r1.route_id))
r3 = builder.build_route('0003', mex, cdg)
print("{} is stored in DB with route_id: {}".format(r3, r3.route_id))
r4 = builder.build_route('0004', cdg, mex)
print("{} is stored in DB with route_id: {}".format(r4, r4.route_id))
r5 = builder.build_route('0005', mex, cdg)
print("{} is stored in DB with route_id: {}".format(r5, r5.route_id))
r6 = builder.build_route('0006', cdg, mex)
print("{} is stored in DB with route_id: {}".format(r6, r6.route_id))
r7 = builder.build_route('0007', mex, lhr)
print("{} is stored in DB with route_id: {}".format(r7, r7.route_id))
r8 = builder.build_route('0008', lhr, mex)
print("{} is stored in DB with route_id: {}".format(r8, r8.route_id))
r10 = builder.build_route('0010', mex, scl)
print("{} is stored in DB with route_id: {}".format(r10, r10.route_id))