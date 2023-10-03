# US City Populations Visualization

Visualize US city populations on a map. Cities are represented by circles sized and colored by population.

![2022 Visualization](docs/2022_map.png)


## Setup
```bash
git clone https://github.com/matteo-psnt/US-city-visualization.git
cd US-city-visualization
pip install -r requirements.txt
```

## Usage
```bash
python3 main.py -year [year] default=2022
```


**Rows seperated by:**            
US Population Rank,               
City,                           
State,              
Population,
Longitude,  
Latitude  


**Sources:**       
Top 100 Biggest US Cities By Population       
https://www.biggestuscities.com/

GeoPy       
https://github.com/geopy/geopy

Run main.py to view a visualization of the data on a map of the US.
