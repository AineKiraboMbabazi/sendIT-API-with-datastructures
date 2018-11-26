import datetime
from .database import DatabaseConnection
con = DatabaseConnection()


class Parcel:
    """
        controller class
    """
    def create_parcel(self, userId, creation_date, status, destination, pickup,
                      present_location, description):
        """
            Function to create parcel delivery order
            :param userId:
            :param creation_date:
            :param status :
            :param pickup :
            :param destination :
            :param present_location :
        """
        add_parcel = "INSERT INTO parcels (userId,creation_date,status,destination,pickup, \
        present_location,description) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        con.cursor.execute(add_parcel, (userId, creation_date, status,
                           destination, pickup, present_location, description))

    def get_all_parcels(self):
        """
            Function to fetch all parcels
        """
        get_all = "SELECT * FROM parcels"
        con.dict_cursor.execute(get_all)
        parcels = con.dict_cursor.fetchall()
        return parcels

    def get_single_parcel(self, parcelId):
        """
            Function to fetch all single parcel
            :param parcelId:
        """
        parcel_query = "SELECT * FROM parcels WHERE parcelId=%s"
        con.dict_cursor.execute(parcel_query, (parcelId,))
        parcel = con.dict_cursor.fetchone()
        return parcel

    def cancel_parcel(self, parcelId):
        """
            Function to cancel parcel
            :param parcelId:
        """
        cancel_query = "UPDATE parcels SET status=%s WHERE parcelId=%s"
        con.cursor.execute(cancel_query, ('Cancelled', parcelId))

    def delete_parcel(self, parcelId):
        """
            Function to delete parcel
            :param parcelId:
        """
        delete_query = "DELETE FROM parcels WHERE parcelId=%s"
        con.cursor.execute(delete_query, (parcelId,))

    def update_present_location(self, parcelId, newlocation):
        """
            Function to update_present_location
            :param parcelId:
            :param newlocation:
        """
        update_query = " UPDATE parcels SET present_location=%s WHERE parcelId=%s"
        con.cursor.execute(update_query, (newlocation, parcelId))

    def update_destination(self, parcelId, newdestination):
        """
            Function to update_destination
            :param parcelId:
            :param newdestination:
        """
        change_destination = "UPDATE parcels SET destination=%s WHERE parcelId=%s"
        con.cursor.execute(change_destination, (newdestination, parcelId))

    def fetch_parcels_by_user(self, userId):
        """
            Function to fetch all parcels by a user
            :param userId:
        """
        fetch_parcels_by_user = "SELECT * FROM parcels WHERE userId=%s"
        con.dict_cursor.execute(fetch_parcels_by_user, (userId,))
        parcels = con.dict_cursor.fetchall()
        return parcels
