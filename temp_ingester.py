import datetime
from meteostat import Point, Daily
from geopy.geocoders import Nominatim
import pandas

class Ingester:
    """ Ingest a given city's historical temperatures for a given time period
        and converts it to a .csv file
        param: city (i.e. London)
        param: start_date (YYYY-M-DD; default = 2010-1-1)
        param: end_date (YYYY-MM-DD; default = current date - 2 days)"""
        
    def __init__(self, city, start_date=None, end_date=None):
        self.city = city
        self.start_date = datetime.datetime(2010, 1, 1) if not start_date else self.convert_date(start_date)
        self.end_date = self.default_end_date() if not end_date else self.convert_date(end_date)
        self.to_csv()

    def __repr__(self):
        return f'City: {self.city}, start date: {self.start_date}, end date: {self.end_date}'

    def get_lat_and_lon(self):
        """ 
        returns: longitude and lattitude of a specified city
        """
        # user agent can be literally anything as it's just a 
        # name for the api to limit calls for the given name
        geolocator = Nominatim(user_agent="test") 
        location = geolocator.geocode(self.city)
        longitude, lattitude = location.latitude, location.longitude
        return longitude, lattitude
    
    def get_historical_data(self):
        """
        returns: Dataframe of historical average temperature for a given city
                 within the specified time period
        """
        lat, lon = self.get_lat_and_lon()
        city = Point(lat, lon)
        data = Daily(city, self.start_date, self.end_date)
        data = data.fetch()
        data = data.filter(['tavg']) # select average temperature column
        data = data.fillna(method='ffill') # fill missing values
        # get a specific day
        #day = data.iloc[lambda x: x.index  == '2014-06-23']
        return data
    
    def to_csv(self):
        """
        Converts the dataframe to a .csv file for a given city
        i.e. London.csv
        """
        data = self.get_historical_data()
        data.to_csv(f'{self.city}.csv', sep='\t', encoding='utf-8')
    
    @staticmethod
    def default_end_date():
        """ 
        returns: yesterday date
        Since the API's latest data point is from 2 days ago, we need yesterday to be
        the end range which is of course not included
        """
        today = datetime.datetime.now()
        difference = datetime.timedelta(days = 1)
        date = today - difference
        end_date = date
        return end_date

    @staticmethod
    def convert_date(date):
        """
        converts a string to a datetime object
        returns: date
        """
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        date = date_obj
        return date

if __name__ == '__main__':
    # usages of the Ingester class
    #obj = Ingester('Birmingham', '2011-3-2', '2020-12-29') #custom dates specified
    obj = Ingester('London') # no date specified (default dates will apply)