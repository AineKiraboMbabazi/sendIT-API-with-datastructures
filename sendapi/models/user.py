from .database import DatabaseConnection
import datetime
con= DatabaseConnection()


class User:
    def get_user_by_email(self,email):
        check_for_unike_email="SELECT * FROM users WHERE email=%s"
        con.cursor.execute(check_for_unike_email,(email,))
        row= con.cursor.fetchone()
        return row

    def get_user_by_id(self,userId):
        get_user="SELECT * FROM users WHERE userId='{0}'".format(userId)
        con.dict_cursor.execute(get_user)
        row= con.dict_cursor.fetchone()
        return row

   
    def get_users(self):
        
        get_all="SELECT * FROM users"
        con.dict_cursor.execute(get_all)
        rows= con.dict_cursor.fetchall()
        return  rows

    def create_user(self, email, password, role):
       
        add_user = "INSERT INTO users (email,password,role) VALUES (%s,%s,%s)"
        con.cursor.execute(add_user,(email,password,role))
        
        
    def delete_user(self,userId):
        delete_user="DELETE FROM users WHERE userId=%s"
        con.cursor.execute(delete_user,(userId,))
   
    def update_user(self,userId):
        update_user=" UPDATE users SET email= newemail WHERE userId=userId"
        con.cursor.execute(update_user)

        