from bs4 import BeautifulSoup
import argparse
import requests
from geopy.geocoders import Nominatim
from alive_progress import alive_bar
from csv import DictReader

parser = argparse.ArgumentParser()
parser.add_argument("-year", help="year's data do you want to find", default=2022)
args = parser.parse_args()
YEAR = args.year

city_pop = open('city_data/city_pop_' + str(YEAR) + '.txt', 'w')
city_pop.write('rank,city,state,population,latitude,longitude\n')
geolocator = Nominatim(user_agent="user")

def find_city_location(city, state):
    with open('city_data/city_location_data.txt') as csvfile:
        dictionary = DictReader(csvfile)

        for row in dictionary:

            if (row['city'] == city and
                    row['state'] == state):
                return dict(row)


PAGE_COUNT = 195
for page_index in range(PAGE_COUNT):
    if YEAR != 2022:
        webData = requests.get('https://www.biggestuscities.com/' + str(YEAR) + '/' + str(page_index + 1))
    else:
        webData = requests.get('https://www.biggestuscities.com/' + str(page_index + 1))

    soup = BeautifulSoup(webData.text, 'lxml')
    tables = soup.findAll('table', 'table-condensed')
    with alive_bar(100, title='Reading Page ' + str(page_index + 1), force_tty=True) as bar:
        for table in tables:
            for row in table.findAll("tr")[0:]:
                cols = row.findAll('td')
                if len(cols) in [3, 4]:
                    rank = cols[0].string
                    city = cols[1].text.split('\n')[1].split(',')[0]
                    state = cols[1].text.split('\n')[1].split(',')[1].lstrip()
                    population = str(cols[2].text.replace(',', '')).strip()

                    city_loc = find_city_location(city, state)
                    if city_loc is not None:
                        longitude = city_loc['longitude']
                        latitude = city_loc['latitude']

                    else:
                        try:
                            loc = geolocator.geocode(city + ',' + state)
                            latitude = str(loc.latitude)
                            longitude = str(loc.longitude)

                        except:
                            latitude = 'None'
                            longitude = 'None'

                    line = (rank, city, state, population, latitude, longitude)
                    city_pop.write(','.join(line) + '\n')
                    bar()
