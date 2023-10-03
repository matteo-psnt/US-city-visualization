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
df = pd.read_csv(f'city_data/city_pop_{YEAR}.csv')
df['text'] = df['city'] + ', ' + df['state'] + '<br>Population ' + (df['population'] / 1e6).astype(str) + ' million'

# Update limits to reflect population values and give numeric names
population_brackets = {
    '5M+': (5000001, 1000000000),
    '1M+': (1000001, 5000000),
    '500K-1M': (500001, 1000000),
    '100K-500K': (100001, 500000),
    '50K-100K': (50001, 100000),
    '0-50K': (0, 50000)
}

# Original colors reversed
colors = ["white", "royalblue", "crimson", "lightseagreen", "orange", "lightgrey"]
scale = 5000

fig = go.Figure()

for bracket_name, lim in population_brackets.items():
    df_sub = df[(df['population'] >= lim[0]) & (df['population'] <= lim[1])]
    fig.add_trace(go.Scattergeo(
        locationmode='USA-states',
        lon=df_sub['longitude'],
        lat=df_sub['latitude'],
        text=df_sub['text'],
        marker=dict(
            size=df_sub['population'] / scale,
            color=colors[list(population_brackets.keys()).index(bracket_name)],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode='area'
        ),
        name=bracket_name))

fig.update_layout(
    title_text=str(YEAR) + ' US city populations<br>(Click legend to toggle traces)',
    showlegend=True,
    geo=dict(
        scope='usa',
        landcolor='rgb(217, 217, 217)',
    )
)

fig.show()
