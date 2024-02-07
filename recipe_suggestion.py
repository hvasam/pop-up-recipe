from config import *
from connection import *
from database_operations import *

RECIPE_COLUMN_ID = 'recipe';
INGREDIENT_COLUMN_ID = 'ingredient';
CLOSENESS_NUMBER = 4;

## ingredient must be a string
## returned recipes are in the form of: [(recipe1,).(recipe2,),...]
def get_recipes_that_contain(ingredient, recipe_list):
    if ingredient is None or ingredient == "":
        return [];
    
    if recipe_list is None or recipe_list == []:
        return [];
    
    query_condition = { INGREDIENT_COLUMN_ID : ingredient, RECIPE_COLUMN_ID : ""};

    recipe_list_subset = [];

    for recipe in recipe_list:
        query_condition[RECIPE_COLUMN_ID] = recipe[0];

        cursor = get_rows_from_database(connection, DEFAULT_DATABASE, DEFAULT_TABLE, RECIPE_COLUMN_ID, query_condition, "AND");

        if cursor is None:
            continue;
    
        recipe_list_subset += cursor.fetchall();

    print("The recipes that use the ingredient: {} given: {} are: {}".format(ingredient, recipe_list, recipe_list_subset));
    return recipe_list_subset;

## ingredient must be a string
## returned recipes are in the form of: [(recipe1,).(recipe2,),...]
def get_recipes_that_do_not_contain(ingredient, recipe_list, database_connection):
    if ingredient is None or ingredient == "":
        return [];

    if recipe_list is None or recipe_list == []:
        return [];
        
    query_condition = { INGREDIENT_COLUMN_ID : ingredient };

    recipe_list_subset = [];

    # select distinct recipe from test.cookbook where recipe not in (SELECT DISTINCT recipe FROM test.cookbook WHERE ingredient = 'salt') ;
    # the following statement gets all recipes from cookbook that do not contain ingredient
    execution_statement = "SELECT DISTINCT {} FROM {} WHERE {} NOT IN (SELECT DISTINCT {} FROM {} WHERE {} = %s)".format(RECIPE_COLUMN_ID,
                                                                                                                         DEFAULT_TABLE,
                                                                                                                         RECIPE_COLUMN_ID,
                                                                                                                         RECIPE_COLUMN_ID,
                                                                                                                         DEFAULT_TABLE,
                                                                                                                         INGREDIENT_COLUMN_ID);
    cursor = database_connection.cursor();
    cursor.execute(execution_statement, (ingredient,));

    if cursor is None:
        return [];

    row = cursor.fetchone();

    while row is not None:
        for recipe in recipe_list:
            if row[0] == recipe[0]:
                recipe_list_subset += (row,);
        row = cursor.fetchone();

    cursor.close();

    print("The recipes that do not use the ingredient: {} given: {} are: {}".format(ingredient, recipe_list, recipe_list_subset));
    return recipe_list_subset;


# set_of_recipes is a mysql cursor object that contains the result of a previous query
def get_recipe_that_requires_less_than_max_ingredients(database_connection, table_name, max_ingredients, set_of_recipes):
    if set_of_recipes is None:
        return "";

    cursor = database_connection.cursor();

    for recipe in set_of_recipes:
        recipe_name = recipe[0];
        execution_statement = "SELECT {}, count(*) AS count FROM {} WHERE {} = %s GROUP BY {} HAVING count < {}".format(RECIPE_COLUMN_ID, table_name, RECIPE_COLUMN_ID, RECIPE_COLUMN_ID, max_ingredients);
        print(execution_statement % recipe_name);

        cursor.execute(execution_statement, (recipe_name,));
        satisfactory_recipes = cursor.fetchall();
        if len(satisfactory_recipes) == 0:
            continue;
        else:
            cursor.close();
            return satisfactory_recipes[0][0];

    return "";


# set_of_recipes is the cursor object containing the results of a query to cookbook table
# found_recipe is an object of [(recipe1,)]
def find_closest_recipe_given_ingredients(database_connection, table_name, ingredient_list, ingredient_list_index, total_number_of_ingredients, total_ingredient_matches, list_of_recipes, found_recipe):

    if found_recipe[0] != "":
        return;
    
    if list_of_recipes is None or list_of_recipes == []:
        return;
    
    if not (ingredient_list_index < total_number_of_ingredients):
        found_recipe[0] = get_recipe_that_requires_less_than_max_ingredients(database_connection, table_name, total_ingredient_matches + CLOSENESS_NUMBER, list_of_recipes);
        return;
    
    print("We will recurse");
    find_closest_recipe_given_ingredients(database_connection, 
                                          table_name, 
                                          ingredient_list, 
                                          (ingredient_list_index + 1), 
                                          total_number_of_ingredients,
                                          (total_ingredient_matches + 1), 
                                          get_recipes_that_contain(ingredient_list[ingredient_list_index], list_of_recipes), # this function needs to be able to recursively find set of recipes 
                                          found_recipe);
    find_closest_recipe_given_ingredients(database_connection, 
                                          table_name, 
                                          ingredient_list, 
                                          (ingredient_list_index + 1), 
                                          total_number_of_ingredients, 
                                          total_ingredient_matches,
                                          get_recipes_that_do_not_contain(ingredient_list[ingredient_list_index], list_of_recipes, connection), # this function needs to be able to recursively find set of recipes 
                                          found_recipe);



def get_missing_ingredients_needed_for_recipe(database_connection, recipe, list_of_ingredients):
    if recipe is None or recipe == "":
        return [];
    
    if list_of_ingredients is None or list_of_ingredients == []:
        return [];
    
    cursor = database_connection.cursor();

    concatenated_string_list = "'" + "', '".join(map(str, list_of_ingredients)) + "'";

    # print("The concatenated string list is: {}".format(concatenated_string_list));
    # select ingredient from test.cookbook where recipe = 'shepherd\'s pie' and ingredient not in ("butter") ;
    execution_statement = "SELECT DISTINCT {} FROM {} WHERE {} = %s AND {} NOT IN ({})".format(INGREDIENT_COLUMN_ID,
                                                                                               DEFAULT_TABLE,
                                                                                               RECIPE_COLUMN_ID,
                                                                                               INGREDIENT_COLUMN_ID,
                                                                                               concatenated_string_list);

    cursor.execute(execution_statement, (recipe,));

    if cursor is None:
        return [];

    rows = cursor.fetchall();
    print("Returned rows are: {}".format(rows))

    return rows;


# cart is a list of items (i.e ingredients) from the customer shopping cart. This list should only contain valid items (produce, meat, dairy, bread, spices etc...).
def get_recipe_and_ingredients_needed_given_cart(database_connection, table_name, cart, recipe_catalog):
    closest_recipe = [""];
    find_closest_recipe_given_ingredients(connection,
                                        table_name,
                                        cart,
                                        ingredient_list_index=0,
                                        total_number_of_ingredients=len(cart),
                                        total_ingredient_matches=0,
                                        list_of_recipes=recipe_catalog,
                                        found_recipe=closest_recipe);

    print("The closest recipe is: {}".format(closest_recipe[0]));
    missing_ingredients = get_missing_ingredients_needed_for_recipe(connection, closest_recipe[0], cart);
    print("The missing ingredients are: {}".format(missing_ingredients));
    return closest_recipe[0], 





# get connection
connection = get_connection_for_db(CONNECTION_DETAILS);
print("Connection was successful");

all_recipes = get_rows_from_database(connection,
                                     DEFAULT_DATABASE,
                                     DEFAULT_TABLE,
                                     RECIPE_COLUMN_ID,
                                     {}).fetchall();

ingredient_list1 = ["salt", "lime juice", "red onion", "Mary", "Larry", "tomatoes", "fresh cilantro", "garlic", "toothbrush"];
ingredient_list2 = ["egg noodles", "broccoli", "bell peppers", "carrots", "snow peas", "ginger", "garlic"];
ingredient_list3 = ["Mary", "Luke", "John", "garlic"];

get_recipe_and_ingredients_needed_given_cart(connection, DEFAULT_TABLE, ingredient_list1, all_recipes);

# close connection
connection.close();