from data.database import Database
from models.sheduleclasses import Airport

Database.initialise(database="tripper", user="Xico", password="semiconductor",
                    host="tripper.cpccqvkq54qu.us-east-2.rds.amazonaws.com")
airport = Airport.load_from_db('MEX')
print(airport)