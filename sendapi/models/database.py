import psycopg2
import psycopg2.extras
from flask import Flask

import os
app=Flask(__name__)

class DatabaseConnection:
    def __init__(self):
        """
            constructor to create a db connection
            :param dbname:
            :param user:
            :param password :
        """
        self.con_parameter=dict(
            database="sendit",
            user="postgres",
            password="postgres"
        )
        self.con=psycopg2.connect(**self.con_parameter)
        self.con.autocommit=True
        self.cursor= self.con.cursor()
        self.dict_cursor=self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def create_db_tables(self):
        """
            Create users table
        """
        create_users_table=(
            """CREATE TABLE IF NOT EXISTS
            users(
                userId SERIAL PRIMARY KEY NOT NULL,
                email VARCHAR(50) UNIQUE,
                password VARCHAR(100) NOT NULL,
                role VARCHAR(20) NOT NULL
            );"""
        )

        create_parcels_table=(
            """CREATE TABLE IF NOT EXISTS
            parcels(
                parcelId SERIAL PRIMARY KEY NOT NULL,
                userId INTEGER,
                status VARCHAR(20),
                creation_date TIMESTAMP,
                destination VARCHAR(30),
                pickup VARCHAR(30),
                present_location VARCHAR(30),
                FOREIGN KEY (userId) REFERENCES users(userId)ON UPDATE CASCADE
                );""")

        # execute cursor object to create tables
        self.cursor.execute(create_users_table)
        self.cursor.execute(create_parcels_table)


    def drop_table(self,table_name):
        """ 
            truncate a table
            :param table_name:
        """
        self.cursor.execute("TRUNCATE TABLE {} RESTART IDENTITY CASCADE".format(table_name))

        # self.cursor.execute("DROP TABLE users;")
if __name__ == '__main__':
    con=DatabaseConnection()
    con.create_db_tables()