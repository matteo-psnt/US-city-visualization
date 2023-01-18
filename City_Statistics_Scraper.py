#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from geopy.geocoders import Nominatim
from alive_progress import alive_bar

# city_pop = open('city_pop.txt', 'w')
# city_pop.write('rank,city,state,population,growth,latitude,longitude\n')
geolocator = Nominatim(user_agent="user")
for page in range(195):
    a = requests.get("https://www.biggestuscities.com/" + str(page + 1))
    soup = BeautifulSoup(a.text, 'lxml')
    # print(soup)
    tables = soup.findAll('table', 'table-condensed')
    # print(tables)
    with alive_bar(100, title='Reading Page ' + str(page + 1)) as bar:
        for table in tables:
            for row in table.findAll("tr")[0:]:
                cols = row.findAll('td')
                if len(cols) == 4:
                    rank = cols[0].string
                    city = cols[1].text.split('\n')[1].split(',')[0]
                    state = cols[1].text.split('\n')[1].split(',')[1]
                    population = str(cols[2].text.replace(',', '')).strip()
                    growth = cols[3].text.replace(',', '').strip()
                    loc = geolocator.geocode(city + ',' + state)
                    try:
                        latitude = str(loc.latitude)
                        longitude = str(loc.longitude)
                    except:
                        latitude = 'None'
                        longitude = 'None'
                    line = (rank, city, state, population, growth, latitude, longitude)
                    # city_pop.write(','.join(line) + '\n')
                    bar()