import datetime

from flask import jsonify, request

parcels = [
#      {
#         'parcelId' : 1,
#         'userId':2,
#         'status':'intransit',
#         'creation_date': '1/11/2018',
#         'pickup': 'jinja',
#         'destination': 'entebbe'
#     },
#     {
#         'parcelId' : 2,
#         'userId':1,
#         'status':'intransit',
#         'creation_date': '1/11/2018',
#         'pickup': 'jinja',
#         'destination': 'katabi'
#     },
#     {
#         'parcelId' : 3,
#         'userId':1,
#         'status':'intransit',
#         'creation_date': '1/11/2018',
#         'pickup': 'jinja',
#         'destination': 'entebbe'
#     }
]
users = []


class Users:
    

    def auto_increment_id(self):
        if not users:
            return 1
        return users[-1]['userId']+1

    def create_user(self):
        request_data = request.get_json(force=True)

        user = dict()
        user['userId'] = self.auto_increment_id()
        user['email'] = request_data['email']
        user['password'] = request_data['password']
        
        return user

    def get_users(self):
        if len(users) > 0:
            return users
        
        return {"message":"No users have been created"}

def reset_parcels():
        parcels.clear()
class Parcels:
    
    
    def get_parcels(self):
        if len(parcels) > 0:
            return parcels
        return {"message":"No parcels have been found"}
    def auto_increment_id(self):
        if not parcels:
            return 1
        return parcels[-1]['parcelId']+1

    def create_parcel(self):
        request_data = request.get_json(force=True)

        parcel = dict()
        parcel['parcelId'] = self.auto_increment_id()
        parcel['userId'] = request_data['userId']
        parcel['status'] = request_data['status']
        parcel['creation_date'] = datetime.date.today().strftime('%Y-%m-%d')
        parcel['pickup'] = request_data['pickup']
        parcel['destination'] = request_data['destination']
        if not parcel['status'] and parcel['userId'] and parcel['destination'] and parcel['pickup']:
            return {"message":"some expected field was not filled"}
        parcels.append(parcel)
        return parcel, {"message":"Your order has been created"}


    def get_specific_parcel(self, parcelId):
     
        for parcel in parcels:
            if parcel['parcelId'] == parcelId:
                return parcel
        return {"message":"The parcel with that id doesnot exist"}

    def get_parcels_by_specific_user(self, userId):
        
        newparcel=list()
        message={"message":"The user with that Id has not created any parcel Delivery orders"}
        for parcel in parcels:
            if parcel['userId'] == userId:
               newparcel.append(parcel)
               if len(newparcel)>1:
                   message={"Created by":userId,"Number of parcels":len(newparcel)}
        return message,newparcel
        
        

    def cancel_specific_parcel(self, parcelId):
        
        for parcel in parcels:
            if parcel['parcelId'] == parcelId:
                parcel['status']='canceled'
                return {"message": "parcel delivery order has been canceled"},parcel
        return {"message":"The order you are trying to cancel doesnot exist"}

