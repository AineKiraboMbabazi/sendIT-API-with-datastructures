import datetime
from .database import DatabaseConnection
con = DatabaseConnection()


class Parcel:
    def create_parcel(self,userId,creation_date, status, destination, pickup, present_location):
        add_parcel = "INSERT INTO parcels (userId,creation_date,status,destination,pickup,present_location) VALUES (%s,%s,%s,%s,%s,%s)"
        con.cursor.execute(add_parcel, (userId,creation_date, status, destination, pickup, present_location))

    def get_all_parcels(self):
        get_all = "SELECT * FROM parcels"
        con.dict_cursor.execute(get_all)
        parcels = con.dict_cursor.fetchall()
        return parcels

    def get_single_parcel(self, parcelId):
        parcel_query = "SELECT * FROM parcels WHERE parcelId=%s"
        con.dict_cursor.execute(parcel_query, (parcelId,))
        parcel = con.dict_cursor.fetchone()
        return parcel

    def cancel_parcel(self, parcelId):
        cancel_query = "UPDATE parcels SET status=%s WHERE parcelId=%s"
        con.cursor.execute(cancel_query, ('Cancelled', parcelId))

    def delete_parcel(self, parcelId):
        delete_query = "DELETE FROM parcels WHERE parcelId=%s"
        con.cursor.execute(delete_query, (parcelId,))

    def update_present_location(self, parcelId, newlocation):
        update_query = " UPDATE parcels SET present_location=%s WHERE parcelId=%s"
        con.cursor.execute(update_query, (newlocation, parcelId))

    def update_destination(self, parcelId, newdestination):
        change_destination = "UPDATE parcels SET destination=%s WHERE parcelId=%s"
        con.cursor.execute(change_destination, (newdestination, parcelId))

    def fetch_parcels_by_user(self, userId):
        fetch_parcels_by_user = "SELECT * FROM parcels WHERE userId=%s"
        con.dict_cursor.execute(fetch_parcels_by_user, (userId,))
        parcels=con.dict_cursor.fetchall()
        return parcels