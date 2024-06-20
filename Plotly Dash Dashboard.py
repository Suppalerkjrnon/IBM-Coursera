import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the data
spacex_df = pd.read_csv('spacex_launch_dash.csv')

# Initialize the app
app = dash.Dash(__name__)

# Dropdown options, use unique values from 'Launch Site' column, this will be create a list of all unique launch sites
dropdown_options = spacex_df['Launch Site'].unique()

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # Dropdown for Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All Sites', 'value': 'ALL'}] +
                                                     [{'label': i, 'value': i} for i in dropdown_options],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                             ),
                                # Pie chart for total successful launches count
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # Placeholder for payload slider (TASK 3)
                                dcc.RangeSlider(id='payload-slider', min=spacex_df['Payload Mass (kg)'].min(), max=spacex_df['Payload Mass (kg)'].max(), step=1000, value=[0, spacex_df['Payload Mass (kg)'].max()]),

                                # Scatter chart for correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# Callback for updating pie chart based on dropdown selection
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        filtered_space_df = spacex_df.groupby('class').size().reset_index(name='class count')
        fig = px.pie(filtered_space_df, values='class count', names='class', title='Total Success vs. Failed Launches for All Sites')
    else:
        filtered_space_df = spacex_df[spacex_df['Launch Site'] == selected_site].groupby('class').size().reset_index(name='class count')
        fig = px.pie(filtered_space_df, values='class count', names='class', title=f'Success vs. Failed Launches for {selected_site}')
    return fig

# Placeholder callback for scatter chart based on payload slider and dropdown (TASK 4)
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    filtered_space_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    if selected_site != 'ALL':
        filtered_space_df = filtered_space_df[filtered_space_df['Launch Site'] == selected_site]
    
    fig = px.scatter(filtered_space_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title='Correlation between Payload and Success for All Sites' if selected_site == 'ALL' else f'Correlation between Payload and Success for {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()