# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Br(),

    # Launch Site Dropdown
    html.Div([
        dcc.Dropdown(id='site-dropdown',
                     options=[
                         {'label': 'All Sites', 'value': 'ALL'},
                         {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                         {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                         {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                         {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                     ],
                     value='ALL',
                     placeholder='Select a Launch Site',
                     searchable=True
                     ),
        html.Br(),
    ]),

    # Pie Chart for Success Counts
    html.Div([
        dcc.Graph(id='success-pie-chart')
    ]),

    html.Br(),

    # Payload Range Slider
    html.Div([
        html.P("Payload range (Kg):"),
        dcc.RangeSlider(id='payload-slider',
                        min=int(min_payload),
                        max=int(max_payload),
                        step=1000,
                        marks={i: '{}'.format(i) for i in range(int(min_payload), int(max_payload) + 1, 1000)},
                        value=[min_payload, max_payload]
                        ),
    ]),

    html.Br(),

    # Scatter Plot for Payload vs. Launch Outcome
    html.Div([
        dcc.Graph(id='success-payload-scatter-chart')
    ])
])

# Callback function to update charts based on selected launch site and payload range
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def update_charts(selected_site, payload_range):
    # Pie Chart
    if selected_site == 'ALL':
        # Calculate success counts for all sites
        site_counts = spacex_df.groupby('Launch Site')['class'].value_counts().unstack(fill_value=0).reset_index()
        site_counts['Total'] = site_counts[0] + site_counts[1]
        site_counts = site_counts.melt(id_vars='Launch Site', value_vars=[0, 1], value_name='Count', var_name='Outcome')
        site_counts['Outcome'] = site_counts['Outcome'].map({0: 'Failure', 1: 'Success'})
        pie_labels = site_counts['Launch Site'] if 'Launch Site' in site_counts.columns else ['Success', 'Failure']
        pie_values = site_counts['Count']
        pie_title = 'Total Success and Failure Counts for All Sites'
    else:
        # Filter dataframe for the selected site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Calculate success and failure counts for the selected site
        success_count = len(site_data[site_data['class'] == 1])
        failure_count = len(site_data[site_data['class'] == 0])
        pie_labels = ['Success', 'Failure']
        pie_values = [success_count, failure_count]
        pie_title = f'Success and Failure Counts for {selected_site}'

    pie_fig = px.pie(names=pie_labels, values=pie_values, title=pie_title)

    # Scatter Plot
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    scatter_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Launch Site',
                             title='Payload vs. Launch Outcome', labels={'class': 'Launch Outcome'})
    
    return pie_fig, scatter_fig

# Run the app
if __name__ == '__main__':
    app.run_server()
