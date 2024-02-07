import mysql.connector

# database_connection is a MySQLConnection Class object
def create_database(database_connection, database_name):
    
    if database_connection is None:
        return;

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


# database_connection is a MySQLConnection Class object
# table_spec is a dictionary that maps column names and SQL data types
def create_table(database_connection, database_name, table_name, table_spec):
    
    if database_connection is None:
        return;

    if database_name is None or database_name == "":
        return;

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
        cursor.close();
        print("Successfully created table: {}".format(table_name));

    except mysql.connector.Error as err:
        print("There was an error when attempting to create the following table: {}".format(table_name));
        print("Failed with error: {}".format(err));






def get_column_names(row):
    columns = '';
    for column in row.keys():
        columns += column;
        columns += ',';
    columns = columns[:-1];
    return columns

# database_connection is a MySQLConnection Class object
# table_spec is a dictionary that maps column names and SQL data types
# row paramater is a dictionary mapping column names to values
def add_row_to_table(database_connection, cursor, database_name, table_name, table_spec, row):
    
    if database_connection is None:
        return;

    if database_name is None or database_name == "":
        return;

    if table_name == "" or table_spec is None or len(table_spec) == 0:
        return;

    if row is None or len(row) != len(table_spec):
        return;

    try:
        database_connection.database = database_name;

        columns = get_column_names(row);
        values = "";

        for value in row.values():
            values += "%s,";

        values = values[:-1];

        # print("Executing following query:");
        # print("INSERT INTO {} ({}) VALUES ({})".format(table_name, columns, values));

        execution_statement = "INSERT INTO {} ({}) VALUES ({})".format(table_name, columns, values);
        values_list = list(row.values());

        print("The execution statement is: {}".format(execution_statement));
        print("The above statement uses the following values: {}".format(values_list))

        # print("The row values are: {}".format(list(row.values())));
        cursor.execute(execution_statement, values_list);

        print("Successfully added row: {}".format(row));
    except mysql.connector.Error as err:
        print("Failed to add row: {} to table: {}".format(row, table_name));
        print("Failed with error: {}".format(err));




def add_primary_key_to_table(database_connection, database_name, table_name, primary_key):

    if database_connection is None:
        return;

    if database_name is None or database_name == "":
        return;
    
    if table_name is None or table_name == "":
        return;
    
    if primary_key is None or primary_key == "":
        return;
    
    try:
        database_connection.database = database_name
        cursor = database_connection.cursor()

        execution_statement = "ALTER TABLE {} ADD PRIMARY KEY {}".format(table_name, primary_key);
        cursor.execute(execution_statement);
        cursor.close();

        print("Successfully added primary key: {} to table: {}".format(primary_key, table_name));
    except mysql.connector.Error as err:
        print("Failed to add primary key: {} to table: {}".format(primary_key, table_name));
        print("Failed with error: {}".format(err));





def generate_where_clause(column_ids_and_values, logical_operator="AND", negate=False):
    if column_ids_and_values is None or column_ids_and_values  == {}:
        return "";
    

    where_clause = "WHERE (";

    if negate == True:
        where_clause = "WHERE NOT (";
    
    for column_id,value in column_ids_and_values.items():
        where_clause += "{} = %s {} ".format(column_id, logical_operator);
    where_clause = where_clause[:-4];
    where_clause += ")";

    return where_clause;

## desired_columns parameter is a string that contains the desired columns (comma delimited)
## column_ids_and_values parameter is a dictionary of column ids and corresponding values to be used in the where clause
def get_rows_from_database(database_connection, database_name, table_name, desired_columns, column_ids_and_values, logical_operator="AND", negate=False):

    if database_connection is None:
        return;

    if database_name is None or database_name == "":
        return;
    
    if table_name is None or table_name == "":
        return;

    try:
        database_connection.database = database_name;
        cursor = database_connection.cursor();

        where_clause = "";
        if negate == True:
            where_clause = generate_where_clause(column_ids_and_values, logical_operator, True);
        else:
            where_clause = generate_where_clause(column_ids_and_values, logical_operator, False);
        
        execution_statement = "SELECT DISTINCT {} FROM {} {}".format(desired_columns, table_name, where_clause);

        values = tuple(column_ids_and_values.values());

        #print("The values used in the execution statement are: {}".format(values));
        #print("The execution statement is: {}".format(execution_statement));

        cursor.execute(execution_statement, values);
        
        return cursor;
    except mysql.connector.Error as err:
        print("Failed to query column ids and values: {} from table: {}".format(column_ids_and_values, table_name));
        print("Failed with error: {}".format(err));