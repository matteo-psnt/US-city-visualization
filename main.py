import ssl
import argparse
import pandas as pd
import plotly.graph_objects as go

ssl._create_default_https_context = ssl._create_unverified_context

parser = argparse.ArgumentParser()
parser.add_argument("-year", help="year you want shown Options: [2022, 2019]", default=2022)
args = parser.parse_args()
YEAR = args.year

# Import City Population data
df = pd.read_csv('city_data/city_pop_' + str(YEAR) + '.txt')
df.head()

df['text'] = df['city'] + ', ' + df['state'] + '<br>Population ' + (df['population'] / 1e6).astype(str) + ' million'
limits = [(0, 5), (6, 10), (11, 20), (21, 100), (101, 1000)]
colors = ["royalblue", "crimson", "lightseagreen", "orange", "lightgrey"]
cities = []
scale = 5000

fig = go.Figure()

for i in range(len(limits)):
    lim = limits[i]
    df_sub = df[lim[0]:lim[1]]
    fig.add_trace(go.Scattergeo(
        locationmode='USA-states',
        lon=df_sub['longitude'],
        lat=df_sub['latitude'],
        text=df_sub['text'],
        marker=dict(
            size=df_sub['population'] / scale,
            color=colors[i],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode='area'
        ),
        name='{0} - {1}'.format(lim[0], lim[1])))

fig.update_layout(
    title_text=str(YEAR) + ' US city populations<br>(Click legend to toggle traces)',
    showlegend=True,
    geo=dict(
        scope='usa',
        landcolor='rgb(217, 217, 217)',
    )
)

fig.show()
