# This module will be used to support reading recipes from CSV files
# The first value in each line will be the recipe name. Each subsequent value on the same line will be the ingredient used in the recipe
# Suppose we have a sample recipe: chicken pot pie
# And suppose, these are the ingredients in a chicken pot pie: butter, onion, all-purpose flour, chicken broth, milk, chicken, peas, carrots, potatoes, double-crust pie pastry
# Sample File Format:
###################################### BEGINNING OF FILE ######################################
# chicken pot pie, butter, onion, all-purpose flour, chicken broth, milk, chicken, peas, carrots, potatoes, double-crust pie pastry
# lasagna, sweet italian sausage, lean ground beef, onion, cloves garlic, crushed tomatoes, canned tomato sauce, tomato paste, fresh parsley, dried basil leaves, italian seasoning, fennel seeds, lasagna noodles, ricotta cheese, mozzarella cheese, parmesan cheese
# cajun seafood pasta, dry fettuccine pasta, heavy whipping cream, green onions, parsley, fresh basil, fresh thyme, red pepper flakes, white pepper, shrimp, scallops, swiss cheese, parmesan cheese
######################################     END OF FILE   ######################################

import csv
from database_operations import add_row_to_table

# database_connection is a MySQLConnection Class object
# table_spec is a dictionary that maps column names and SQL data types
def upload_recipes_csv_to_database(database_connection, cursor, database_name, table_name, table_spec, path_to_recipes_file):

    if database_connection is None:
        return;

    if database_name is None or database_name == "":
        return;

    if table_name == "" or table_spec is None or len(table_spec) == 0:
        return;

    with open(path_to_recipes_file, newline='') as f:
        reader = csv.reader(f);
        for row in reader:
            number_of_items = len(row);
            if number_of_items < 2:
                continue;

            # print("The current row is: {}".format(row));
            recipe_name = row[0];
            for index in range(number_of_items):
                # print("The current index is: {}".format(index));
                if index == 0:
                    continue;
                else:
                    # print("The row being added to the database is: {} : {}".format(recipe_name, row[index]));
                    current_row = {'recipe' : row[0].lower().strip(), 
                                   'ingredient' : row[index].lower().strip()};
                    add_row_to_table(database_connection, cursor, database_name, table_name, table_spec, current_row);