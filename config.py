# store database connection values here


HOST = 'localhost';
PORT = '3306';
USERNAME = 'root';
PASSWORD = 'my-secret-pw';

DATABASE = 'test';

# this dictionary contains a mapping between table names and a dictionary consisting of a mapping between columns names and column data types. 
TABLES = {
            'cookbook' : { 
                            'recipe' : 'VARCHAR(128)',
                            'ingredient' : 'VARCHAR(64)'
                        }
};

ROW = {'recipe' : 'Shepherd\'s Pie', 'ingredient' : 'Minced Meat'};


CONNECTION_DETAILS = {
    'host' : HOST,
    'port' : PORT,
    'user' : USERNAME,
    'password' : PASSWORD
}