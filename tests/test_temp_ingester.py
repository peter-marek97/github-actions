import unittest
from temp_ingester import Ingester
import os
import pandas as pd
from datetime import datetime

class TestIngester(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.obj = Ingester('London') # no date specified (default dates will apply)
        cls.obj2 = Ingester('Manchester', '2011-3-2', '2020-12-29') #custom dates specified
        cls.file1 = cls.obj.city + ".csv"
        cls.file2 = cls.obj2.city + ".csv"
        cls.data1 = pd.read_csv(cls.file1, parse_dates=["time"], index_col="time", delimiter='\t')
        cls.data2 = pd.read_csv(cls.file2, parse_dates=["time"], index_col="time", delimiter='\t')
        cls.lat_lon1 = cls.obj.get_lat_and_lon()
        cls.lat_lon2 = cls.obj2.get_lat_and_lon()

    
    @classmethod
    def tearDownClass(cls):
        if os.path.isfile(cls.file1): os.remove(cls.file1)
        if os.path.isfile(cls.file2): os.remove(cls.file2)

    def test_city_instance(self):
        self.assertEqual(self.obj.city, 'London')
        self.assertEqual(self.obj2.city, 'Manchester')

    def test_start_and_end_date(self):
        date1_start = self.data1.first_valid_index().date()
        date1_compare = datetime.strptime("2010/01/01", "%Y/%m/%d").date()
                
        date2_start = self.data2.first_valid_index().date()
        date2_compare = datetime.strptime("2011/03/02", "%Y/%m/%d").date()
        
        date2_end = self.data2.last_valid_index().date()
        date2_end_compare = datetime.strptime("2020/12/29", "%Y/%m/%d").date()

        self.assertEqual(date1_start, date1_compare)
        self.assertEqual(date2_start, date2_compare)
        self.assertEqual(date2_end, date2_end_compare)
    
    def file_exists(self):
        self.assertTrue(os.path.isfile(self.file1))
        self.assertTrue(os.path.isfile(self.file2))

    def is_dataframe(self):
        self.assertIsInstance(self.data1, pd.DataFrame)
        self.assertIsInstance(self.data2, pd.DataFrame)
    
    def column_present(self):
        self.assertEqual(self.data1.columns[0], "tavg")
        self.assertEqual(self.data2.columns[0], "tavg")
    
    def test_lat_lon(self):
        self.assertIsInstance(self.lat_lon1, tuple)
        self.assertIsInstance(self.lat_lon2, tuple)