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
#launch_sites = [i for i in spacex_df['Launch Site']]
launch_sites = [{'label':'All Sites', 'value':'ALL'}]
launch_sites.extend([{'label':i,'value':i} for i in spacex_df['Launch Site'].unique()])

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=launch_sites,
                                             #options=[{'label':i,'value':i} for i in spacex_df['Launch Site'].unique()],
                                             value='ALL',
                                             placeholder='ALL',
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000,
                                                marks={i:'{}'.format(i) for i in range(0,10000,2500)},
                                                tooltip={'placement': 'top', 'always_visible': True},
                                                value=[0,10000], updatemode='drag'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))

def pie_chart(site_selected):
    if site_selected=='ALL' or site_selected==None:
        fig=px.pie(spacex_df.groupby('Launch Site').sum().reset_index(), values='class', names='Launch Site', title='Total Success Launches by Site')
        return fig
    else:      
        fig=px.pie(spacex_df[spacex_df['Launch Site']==site_selected].groupby('class').size().reset_index(), values=0, names='class', title='Total Success Launches for Site {}'.format(site_selected))
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown','value'), Input('payload-slider','value')])

def scatter_chart(site_selected, value):
    if site_selected=='ALL' or site_selected==None:
        fig=px.scatter(spacex_df[(spacex_df['Payload Mass (kg)']>value[0]) & (spacex_df['Payload Mass (kg)']<value[1])], x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for all Sites')
        fig.update_layout(yaxis={'tickvals':[0, 1]})
        return fig
    else:      
        fig=px.scatter(spacex_df[(spacex_df['Payload Mass (kg)']>value[0]) & (spacex_df['Payload Mass (kg)']<value[1]) & (spacex_df['Launch Site']==site_selected)], x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for Site {}'.format(site_selected))
        fig.update_layout(yaxis={'tickvals':[0, 1]})
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
