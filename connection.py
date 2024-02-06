import mysql.connector

def get_connection_for_db(connection_details):
    print("Attempting to establish connection to host {}".format(connection_details['host']));
    try:
        return mysql.connector.connect(**connection_details);
    except mysql.connector.Error as err:
        print("Connection was unsuccessful");
        exit(1)