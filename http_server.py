from typing import List
from fastapi import FastAPI, Query
from connection import get_connection_for_db
from database_operations import get_rows_from_database
from recipe_suggestion import get_recipe_and_ingredients_needed_given_cart, RECIPE_COLUMN_ID, INGREDIENT_COLUMN_ID
from config import CONNECTION_DETAILS, DEFAULT_DATABASE, DEFAULT_TABLE
import mysql.connector

app = FastAPI()

@app.get("/suggest_a_recipe/")
def get_items(item_ids: List[str] = Query(...)):

    connection = get_connection_for_db(CONNECTION_DETAILS);
    print("Connection was successful");
    #print(item_ids)

    all_recipes = get_rows_from_database(connection,
                                         DEFAULT_DATABASE,
                                         DEFAULT_TABLE,
                                         RECIPE_COLUMN_ID,
                                         {}).fetchall();

    if item_ids is None or len(item_ids) == 0:
        return {"":""};

    print("A recipe suggestion request for the following items was received: {}".format(item_ids));
    recipe, missing_ingredient_list = get_recipe_and_ingredients_needed_given_cart(connection, DEFAULT_TABLE, item_ids, all_recipes);
    connection.close();
    return {recipe : missing_ingredient_list}
