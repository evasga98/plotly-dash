import requests
import pandas as pd 

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go


app = Dash(__name__, url_base_pathname='/')
app.title = "SigFox IoT"
server = app.server

r = requests.get(url='http://some/url')
json = r.json()

df = pd.json_normalize(json)
df = df[(df['created_at'] > '2021-01-24 23:00:00')]
df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime('%Y-%m-%d %H:%M')

#-----------------CREATE THE GRAPHS-----------------#
#DHT11 GRAPH
temp = go.Bar(x=df["created_at"], y=df["Field1"], name = "Temperature (ºC)")
humid = go.Bar(x=df["created_at"], y=df["Field2"], name = "Humidity (%)")
dht11 = []
dht11.extend([temp])
dht11.extend([humid])

#BATTERY GRAPH
battery = go.Indicator(
    mode = "gauge+number",
    value = df["Field5"].iloc[-1],
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Battery"},
    gauge = {'axis': {'range': [None, 3.3]},
    'bar': {'color': "#00CC96"}
    })

#INTERNAL TEMP GRAPH
internal_temp = go.Bar(x=df["created_at"], y=df["Field3"], marker_color='#AB63FA',name = "Chip Temperature (ºC)")

#PIR GRAPH
labels = ['1', '0']
pir = df['Field4'].value_counts()/len(df['Field4'])
values = [pir[0],pir[1]]
pir_trace = go.Pie(labels = labels, values = values, hole=.4, marker = {'colors': ['#19D3F3', '#FECB52']})


layout_dht11 = go.Layout(
    title = "DHT11 Sensor Data",
    hovermode='x',
    xaxis= dict(linecolor='black',title = 'Date',)
)

layout_temp = go.Layout(
    title = "Internal Temperature",
    hovermode='x',
    xaxis= dict(linecolor='black',title = 'Date'),
    yaxis= dict(title= "Temperature (ºC)")
)

layout_pir = go.Layout(
    title = "PIR Sensor Data",
)


fig_dht11 = go.Figure(data=dht11, layout=layout_dht11)
fig_battery = go.Figure(data= battery)
fig_temp = go.Figure (data=internal_temp, layout=layout_temp)
fig_pir = go.Figure(data = pir_trace, layout = layout_pir)

#-----------------SHOW THE GRAPHS-----------------#
app.layout = html.Div([

    html.Div([
        html.H2('Trabajo SigFox IoT 20/21 - Eva Sánchez'),
        html.P('Datos recogidos mediante una placa MRKFOX 1200 con id ' + df["id_Sigfox"].iloc[0] + ' y un sensor DHT11',style={ "font-size":22})
    ],style={"margin-left": "20px"}),

    html.Div(dcc.Graph(id='dht11_graph',figure=fig_dht11), style={'width': '65%', 'display': 'inline-block'}),
    html.Div(dcc.Graph(id='battery',figure=fig_battery), style={'width': '25%','display': 'inline-block'}),
    html.Div(dcc.Graph(id='temp_graph',figure=fig_temp), style={'width': '60%', 'display': 'inline-block'}),
    html.Div(dcc.Graph(id='pir_graph',figure=fig_pir), style={'width': '30%','display': 'inline-block'})
    
], style={'width': '95%', 'display': 'inline-block', "margin-left": "20px", "margin-top": "10px"})


if __name__ == '__main__':
    app.run_server(debug=True)
