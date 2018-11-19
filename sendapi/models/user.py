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
        check_for_unike_email="SELECT * FROM users WHERE email=%s"
        con.cursor.execute(check_for_unike_email,(userId,))
        row= con.cursor.fetchone()
        return row
   
    def get_users(self):
        get_all="SELECT * FROM users"
        con.dict_cursor.execute(get_all)
        rows= con.dict_cursor.fetchall()
        for row in rows:
            return  "'%s %s %s %s'" %row['userId'], row['email'],row['password'],row['row']

    def create_user(self, email, password, role):
        try:
            add_user = "INSERT INTO users (email,password,role) VALUES (%s,%s,%s)"
            con.cursor.execute(add_user,(email,password,role))
        
        except Exception:
            return {"message":"connection to the database failed"}


        