import datetime

"""list to store the parcels"""
parcels=[]


class Parcel:
    def __init__(self, userId,status,pickup,destination):
        self.parcelId= len(parcels)+1
        self.userId= userId
        self.status= status
        self.creation_date= datetime.date.today().strftime('%Y-%m-%d')
        self.pickup= pickup
        self.destination=destination

    """Function to create parcel dictionary"""
    def to_dictionary(self):
        parcel = {
            "parcelId" : self.parcelId,
            "userId" : self.userId,
            "status":self.status,
            "creation_date": self.creation_date,
            "pickup" :self.pickup,
            "destination": self.destination
        }
        return parcel


