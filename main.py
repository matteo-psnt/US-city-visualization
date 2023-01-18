import ssl

import plotly.graph_objects as go

ssl._create_default_https_context = ssl._create_unverified_context
import pandas as pd

df = pd.read_csv('city_pop.txt')
df.head()

df['text'] = df['city'] + ', ' + df['state'] + '<br>Population ' + (df['population'] / 1e6).astype(str) + ' million'
limits = [(0, 5), (6, 10), (11, 20), (21, 100), (100, 3000)]
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
    title_text='2019 US city populations<br>(Click legend to toggle traces)',
    showlegend=True,
    geo=dict(
        scope='usa',
        landcolor='rgb(217, 217, 217)',
    )
)

fig.show()
