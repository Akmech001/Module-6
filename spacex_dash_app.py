# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
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
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div([
                                    dcc.Graph(id='success-pie-chart'),
                                    html.Br(),
                                    dcc.Graph(id='success-failure-pie-chart')  # Added Success vs. Failure pie chart
                                ]),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_success_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Calculate total success counts for all sites
        total_success = len(spacex_df[spacex_df['class'] == 1])
        labels = ['Success']
        values = [total_success]
        title = 'Total Success Counts for All Sites'
    else:
        # Filter dataframe for the selected site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Calculate success counts for the selected site
        success_count = len(site_data[site_data['class'] == 1])
        labels = ['Success']
        values = [success_count]
        title = f'Success Counts for {selected_site}'
    
    # Create pie chart figure
    fig = px.pie(names=labels, values=values, title=title)
    return fig

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-failure-pie-chart` as output
@app.callback(
    Output(component_id='success-failure-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_success_failure_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Calculate total success and failure counts for all sites
        total_success = len(spacex_df[spacex_df['class'] == 1])
        total_failure = len(spacex_df[spacex_df['class'] == 0])
        labels = ['Success', 'Failure']
        values = [total_success, total_failure]
        title = 'Total Success vs. Failure Counts for All Sites'
    else:
        # Filter dataframe for the selected site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Calculate success and failure counts for the selected site
        success_count = len(site_data[site_data['class'] == 1])
        failure_count = len(site_data[site_data['class'] == 0])
        labels = ['Success', 'Failure']
        values = [success_count, failure_count]
        title = f'Success vs. Failure Counts for {selected_site}'
    
    # Create pie chart figure
    fig = px.pie(names=labels, values=values, title=title)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
    
