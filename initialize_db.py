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
    create_database(connection, DEFAULT_DATABASE);
except mysql.connector.Error as err:
    print("Failed: {}".format(err));

# create tables
try:
    create_table(connection, DEFAULT_DATABASE, DEFAULT_TABLE, TABLES[DEFAULT_TABLE]);
    add_primary_key_to_table(connection, DEFAULT_DATABASE, DEFAULT_TABLE, DEFAULT_TABLE_PRIMARY_KEY);
except mysql.connector.Error as err:
    print("Failed: {}".format(err));

# populate tables
try:
    cursor = connection.cursor();
    upload_recipes_csv_to_database(connection, cursor, DEFAULT_DATABASE, DEFAULT_TABLE, TABLES[DEFAULT_TABLE], DEFAULT_RECIPES_FILE_PATH);
    # Insert statements must be committed
    connection.commit();
    cursor.close();
except mysql.connector.Error as err:
    print("Failed: {}".format(err));

connection.close()
