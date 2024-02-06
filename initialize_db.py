import mysql.connector
from connection import get_connection_for_db
from database_operations import *
from csv_recipe_file_operations import upload_recipes_csv_to_database
from config import *

################################################################################
# use this module to initialize the database, its tables and contents

# get connection
connection = get_connection_for_db(CONNECTION_DETAILS);
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

# populate tables
try:
    upload_recipes_csv_to_database(connection, DATABASE, DEFAULT_TABLE, TABLES[DEFAULT_TABLE], DEFAULT_RECIPES_FILE_PATH)
except mysql.connector.Error as err:
    print("Failed: {}".format(err));


connection.close()
