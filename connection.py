import mysql.connector
from config import *

def get_connection_for_db():
    print("Attempting to establish connection to host {}".format(CONNECTION_DETAILS['host']));
    try:
        return mysql.connector.connect(**CONNECTION_DETAILS);
    except mysql.connector.Error as err:
        print("Connection was unsuccessful");
        exit(1)