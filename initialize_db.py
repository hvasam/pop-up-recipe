import mysql.connector
from connection import get_connection_for_db
from database_operations import *
from config import *

################################################################################
# use this module to initialize the database, its tables and contents

# get connection
connection = get_connection_for_db();
print("Connection was successful");

# create db
try:
    create_database(connection, DATABASE);
except mysql.connector.Error as err:
    print("Failed: {}".format(err));

# create tables
try:
    for table in TABLES:
        create_table(connection, DATABASE, table, TABLES[table]);
except mysql.connector.Error as err:
        print("Failed: {}".format(err));

# populate table


connection.close()
