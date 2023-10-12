# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.Br(),

                                dcc.Dropdown(id='site-dropdown', # TASK 1: Add a dropdown list to enable Launch Site selection
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch Site", style={'width':'80%'}),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')), # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider', # TASK 3: Add a slider to select payload range
                                                min=min_payload,
                                                max=max_payload,
                                                step=1000,
                                                marks={i: str(i) for i in range(int(min_payload), int(max_payload+1), 1000)},
                                                value=[min_payload, max_payload]
                                ),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')), # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                ])

# TASK 2:
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Successful Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', title=f'Successful Launches at {selected_site}')
    return fig

# TASK 4:
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, selected_payload):
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payload[0]) & 
                                (spacex_df['Payload Mass (kg)'] <= selected_payload[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Payload vs. Outcome')
    else:
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payload[0]) & 
                                (spacex_df['Payload Mass (kg)'] <= selected_payload[1]) &
                                (spacex_df['Launch Site'] == selected_site)]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Payload vs. Outcome at {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
