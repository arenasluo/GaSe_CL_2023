import plotly.offline as pyo
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import pandas as pd
import os, glob
import numpy as np
import matplotlib.pyplot as plt
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import time
import plotly.io as pio
import io
import pathlib 


#### import data
network_daylist = []
periods = 29488
date1 = 0
for number in range(periods):
    date1= date1 + 1
    network_daylist.append("{:05d}".format(date1))
    
    
#### import data
PATH = pathlib.Path(__file__).parent.parent
print(PATH)
DATA_PATH = PATH.joinpath("data/dataset.csv").resolve()
print(DATA_PATH)

df_data = pd.read_csv(DATA_PATH).set_index('Wavelength')
#df_data = pd.read_csv(DATA_PATH + 'dataset.csv').set_index('Wavelength')
df_data.columns.values[:]=[i+1 for i in range(len(network_daylist))]
##############



x = np.linspace(1,29488,num=29488)
y = np.linspace(1,29488,num=29488)

kkk = df_data.index.tolist()

xrange = np.linspace(-17.58,17.58,num=194)
yrange = np.linspace(-13.77,13.77,num=152)

xx, yy = np.meshgrid(xrange, yrange)
#z=df_data.T.iloc[:,low:high].sum(axis=1).values.reshape(xx.shape)

layout = go.Layout()

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    [
        html.H4("Integrated intensity"),
        dcc.Graph(id="graph"),
        html.P("Wavelength (nm):"),
        dcc.RangeSlider(
            id="range-slider",
            min=kkk[23],
            max=kkk[449],
            step=0.1,
            marks={i: str(i) for i in range(int(kkk[23]), int(kkk[449]), 10)},
            value=[kkk[35], kkk[106]],
        ),
        # html.A(
        #     html.Button("Download as HTML"),
        #     id="download",
        #     #href="data:text/html;base64," + encoded,
        #     download="plotly_graph.html"
        # ),
        # html.Div(id="download-button"),
    ]
)

@app.callback(
    Output("graph", "figure"),
    #Output('output', 'children')
    Input("range-slider", "value"),
)

def update_chart(slider_range):
    low, high = slider_range
    mask = (df_data.index > low) & (df_data.index < high)
    z = df_data.T.iloc[:, mask].sum(axis=1).values.reshape(xx.shape)

    fig = go.Figure(
        go.Heatmap(
            x=xrange,
            y=yrange,
            z=z,
            zmin = 0,
            zmax = 50000,
            colorscale='Jet',  # https://plotly.com/python/builtin-colorscales/
            colorbar=dict(
                # title='Color bar title',  # title here
                titleside='right',
                titlefont=dict(
                    size=14,
                    family='Arial, sans-serif')
            ),#https://plotly.com/python/contour-plots/#basic-contour-plot
        )
    )

    fig.update_layout(
        autosize=False,
        width=750,
        height=750,
        #range_color = [10000,100000],
        ### caxis
        #coloraxis=dict(colorscale="turbo", cmin=10000, cmax=100000),
        margin=dict(
            l=80,
            r=80,
        ),
    )
    pyo.plot(fig)
    pio.write_html(fig, 'figure.html', auto_open = True)
    #pio.write_html(fig, file=’index.html’, auto_open = True)

    return fig



if __name__ == "__main__":
    app.run_server(debug=False)
