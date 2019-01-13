import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify

import os
app = Flask(__name__)


class DatabaseConnection:
    def __init__(self):
        """
            constructor to create a db connection
            :param dbname:
            :param user:
            :param password :
        """
        try:
            self.con_parameter = dict(
                host="ec2-54-225-110-156.compute-1.amazonaws.com",
                database="d60ul7j7uuis00",
                user="tbvsiihjctcizx",
                password="f1aad00ee06d0276ecc041b6d3ab12fec64132e16b2a7c663d40528bc745b4c8"
            )
            self.con = psycopg2.connect(**self.con_parameter)
            self.con.autocommit = True
            self.cursor = self.con.cursor()
            self.dict_cursor = self.con.cursor(cursor_factory=RealDictCursor)

        except Exception:
            return jsonify({"message": "Cant connect to database"})
    def create_db_tables(self):
        """
            Create users table
        """
        create_users_table = (
            """CREATE TABLE IF NOT EXISTS
            users(
                userId SERIAL PRIMARY KEY NOT NULL,
                email VARCHAR(50) UNIQUE,
                password VARCHAR(100) NOT NULL,
                role VARCHAR(20) NOT NULL
            );"""
        )

        create_parcels_table = (
            """CREATE TABLE IF NOT EXISTS
            parcels(
                parcelId SERIAL PRIMARY KEY NOT NULL,
                userId INTEGER,
                status VARCHAR(20),
                creation_date TIMESTAMP,
                destination VARCHAR(50),
                pickup VARCHAR(50),
                present_location VARCHAR(50),
                description VARCHAR(100),
                FOREIGN KEY (userId) REFERENCES users(userId)ON UPDATE CASCADE
                );""")

        """
            execute cursor object to create tables
        """
        self.cursor.execute(create_users_table)
        self.cursor.execute(create_parcels_table)

    def drop_table(self, table_name):
        """
            truncate a table
            :param table_name:
        """
        self.cursor.execute(
            "TRUNCATE TABLE {} RESTART IDENTITY CASCADE".format(table_name))


if __name__ == '__main__':
    con = DatabaseConnection()
    con.create_db_tables()
