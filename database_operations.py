import mysql.connector

def create_database(database_connection, database_name):
    if database_name is None or database_name == "":
        return;
    try:
        cursor = database_connection.cursor();
        execution_statement = 'CREATE DATABASE {}'.format(database_name);
        cursor.execute(execution_statement);
        cursor.close();
        print("Database creation was successful for database: {}".format(database_name));
    except mysql.connector.Error as err:
        print("Failed to create database: {}".format(database_name));
        print("Failed with error: {}".format(err));

def create_table(database_connection, database_name, table_name, table_spec):
    if table_name == "" or table_spec is None or len(table_spec) == 0:
        return;
    try:
        database_connection.database = database_name;
        cursor = database_connection.cursor();
        
        print("the table spec is: {}".format(table_spec));

        column_statement = "(";
        for column,data_type in table_spec.items():
            column_statement += "{} {},".format(column, data_type);
        column_statement = column_statement[:-1];
        column_statement += ')';

        print("The column statement is: {}".format(column_statement));

        execution_statement = ("CREATE TABLE {} {}").format(table_name, column_statement);
        cursor.execute(execution_statement);
        print("Successfully created table: {}".format(table_name));

    except mysql.connector.Error as err:
        print("There was an error when attempting to create the following table: {}").format(table_name);
        print("Failed with error: {}".format(err));