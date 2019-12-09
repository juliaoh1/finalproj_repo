#Julia Coxen
#SI 507
#Discussion: Tuesday 4pm

## Final Project for SI 507

#Unit testing

import unittest
from finalproj_part3 import *
import sqlite3

class TestDatabase(unittest.TestCase):

    def test_RR_table(self):
        conn = sqlite3.connect('rubratings.db')
        cur = conn.cursor()

        sql = 'SELECT City FROM RR_combined'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Birmingham',), result_list)
        self.assertEqual(len(result_list), 32263)

        sql = 'SELECT DISTINCT City FROM RR_combined'
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 136)
        
        
        sql = "SELECT city, count(pageid) from RR_combined GROUP BY city"
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(result_list[0][0],'Albany') #Albany
        self.assertEqual(result_list[3][1], 84) #Anchorage
        
        sql = "SELECT distinct date from RR_combined"
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 16)

        conn.close()

    def test_cities_table(self):
        conn = sqlite3.connect('rubratings.db')
        cur = conn.cursor()
        
        sql = "SELECT city from cities"
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Ann Arbor',), result_list)
        self.assertEqual(len(result_list), 28896)

        sql = '''
            SELECT city from Cities
            where state_name='Virginia'
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Alexandria',), result_list)
        self.assertEqual(len(result_list), 586)
        
        conn.close()
         
    def test_joins(self):
        conn = sqlite3.connect('rubratings.db')
        cur = conn.cursor()

        sql = '''
            SELECT RR_combined.city, count(RR_combined.pageid) FROM RR_combined 
            JOIN Cities ON RR_combined.locationID= cities.Id
            GROUP BY cities.city
            ORDER BY count(RR_combined.pageid) 
            DESC LIMIT 10
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Atlanta', 1823,), result_list)
        self.assertEqual(result_list[2][1], 1823) #Atlanta
        self.assertEqual(result_list[6][1], 790) #Phoenix
        conn.close()
        
class TestMapSearch(unittest.TestCase):

    def test_map_search(self):
        results = process_command('map')
        self.assertEqual(results[3][0], 'Chicago')
        self.assertEqual(results[1][2], '42.1192') #New York

class TestTimeSearch(unittest.TestCase):

    def test_time_search(self):
        results = process_command('time all')
        self.assertEqual(results[0][0], '2019-11-20')
        self.assertEqual(results[1][1], 300) #New York
        
        results = process_command('time city=Houston')
        self.assertEqual(results[0][0], '2019-11-21')
        self.assertEqual(results[6][1], 88) #Houston

class TestWordsSearch(unittest.TestCase):

    def test_words_search(self):
        results = process_command('words all')
        self.assertIn(str('Masseuse',), results[0][0])

        results = process_command('words state=Arizona')
        self.assertEqual(results[0][0], '                                                                  Welcome To Angel Massage7 Days Open. 9:30-9:30Deep Tissu/ Hot Stone/ Oil Massage/ Foot Reflexology/ AromatherapyCall And Text:                                            ')


unittest.main()
