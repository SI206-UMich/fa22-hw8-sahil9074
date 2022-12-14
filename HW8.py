import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
    pass
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute("SELECT name, building, category, rating FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id JOIN categories ON restaurants.category_id = categories.id")
    restaurant = cur.fetchall()
    restaurants = []
    for x in restaurant:
        dict = {}
        dict['name'] = x[0]
        dict['building'] = x[1]
        dict['category'] = x[2]
        dict['rating'] = x[3]
        restaurants.append(dict)
    return restaurants


def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute("SELECT categories.category, COUNT(*) FROM restaurants JOIN categories ON restaurants.category_id = categories.id GROUP BY Category ORDER BY COUNT(*) ASC")
    count = cur.fetchall()
    conn.commit()
    dict = {}
    for x in count:
        dict[x[0]] = x[1]

    restaurants = list(dict.keys())
    categories = list(dict.values())
    plt.barh(restaurants, categories)
    plt.xlabel("Number of Restaurants")
    plt.ylabel("Categories")
    plt.title("Types of Restaurants on South University Ave")
    plt.tight_layout()
    # plt.show()
    plt.savefig("bar_chart.png")

    return dict

#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar chart that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    
    file_path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(file_path+'/'+db_filename)
    cur = conn.cursor()
    
    cur.execute("SELECT categories.category, AVG(restaurants.rating) FROM restaurants JOIN categories ON restaurants.category_id = categories.id GROUP BY Category ORDER BY AVG(restaurants.rating) DESC")
    
    ratings = cur.fetchall()
    conn.commit()
    highest_rated = ratings[0]
    dict = {}
    for x in ratings:
        dict[x[0]] = x[1]

    categories = list(dict.keys())
    ratings = list(dict.values())

    plt.barh(categories, ratings)
    plt.xlabel("Average Rating")
    plt.ylabel("Categories")
    plt.title("Average Ratings of Restaurant Categories")
    plt.tight_layout()
    plt.yticks(range(len(categories)), categories[::-1])
    plt.savefig("bar_chart_ratings.png")

    return (highest_rated[0], highest_rated[1])

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
