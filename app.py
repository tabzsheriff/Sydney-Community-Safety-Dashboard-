from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import json
import plotly.graph_objects as go

df = pd.read_csv("community_safety_predictions_2025_lga.csv")
df = df[df['LGA'] != "Lord Howe Island"]

geojson = json.load(open("NSW-suburb.geojson", "r", encoding="utf-8"))

# dropdown, checklist options
suburb = sorted(df['LGA'].unique()) 
crime_type = ['Theft', 'Drug', 'Assault', 'Damage']
years = ['2020', '2021', '2022', '2023', '2024']

external_stylesheets = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Define color scheme
BACKGROUND_COLOR = '#2b2f42'  
CARD_COLOR = '#353a50'        
TEXT_COLOR = 'white'

# For Interactive map

nsw_loca_2 = []
count = []
for feature in geojson["features"]:
    nsw_loca_2.append(feature[u'properties'][u'nsw_loca_2'])
    count.append( 0 )

temp = { 'nsw_loca_2': nsw_loca_2, 'Theft_Count_2020': 0, 'Theft_Rate_2020': 0, 'Theft_Count_2021': 0, 'Theft_Rate_2021': 0, 'Theft_Count_2022': 0, 'Theft_Rate_2022': 0, 'Theft_Count_2023': 0, 'Theft_Rate_2023': 0, 'Theft_Count_2024': 0, 'Theft_Rate_2024': 0, 'Damage_Count_2020': 0, 'Damage_Rate_2020': 0, 'Damage_Count_2021': 0, 'Damage_Rate_2021': 0, 'Damage_Count_2022': 0, 'Damage_Rate_2022': 0, 'Damage_Count_2023': 0, 'Damage_Rate_2023': 0, 'Damage_Count_2024': 0, 'Damage_Rate_2024': 0, 'Drug_Count_2020': 0, 'Drug_Rate_2020': 0, 'Drug_Count_2021': 0, 'Drug_Rate_2021': 0, 'Drug_Count_2022': 0, 'Drug_Rate_2022': 0, 'Drug_Count_2023': 0, 'Drug_Rate_2023': 0, 'Drug_Count_2024': 0, 'Drug_Rate_2024': 0, 'Assault_Count_2020': 0, 'Assault_Rate_2020': 0, 'Assault_Count_2021': 0, 'Assault_Rate_2021': 0, 'Assault_Count_2022': 0, 'Assault_Rate_2022': 0, 'Assault_Count_2023': 0, 'Assault_Rate_2023': 0, 'Assault_Count_2024': 0, 'Assault_Rate_2024': 0, 'Safety_Score': 0, 'Model_Safety_Score': 0, 'Adjusted_Safety_Score': 0, 'Color_Code': 0, 'Predicted_Assault_2025': 0, 'Predicted_Drug_2025': 0, 'Predicted_Damage_2025': 0, 'Predicted_Theft_2025': 0,'New_Safety_Score': 0, 'Final_Safety_Score': 0}

df1 = pd.DataFrame(temp)

df2 = df[['nsw_loca_2', 'Theft_Count_2023']]

data = pd.concat([df, df1]).drop_duplicates(subset=['nsw_loca_2'])
data = data[data['nsw_loca_2'] != "LORD HOWE ISLAND"]

def get_top_safest_suburbs():
    """Returns dynamically populated top 3 safest suburbs."""
    top_suburbs = df.nlargest(3, 'Final_Safety_Score')['LGA']
    return html.Ul([
        html.Li(f"{suburb}") 
        for suburb in top_suburbs
    ], style={
        'list-style': 
        'none', 
        'padding': '0', 
        'font-size': '18px', 
        'color': TEXT_COLOR})

# App layout
app.layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            dbc.Row([
                # Dashboard title
                html.H1('Sydney Community Safety Dashboard')
                ], style={'margin': '5px'}),
            
            dbc.Row([
                html.Div([
                    html.H3("Instructions"),
                
                    # Instructions list
                    html.Ul([
                    html.Li('Select a suburb or local government area.', 
                        style={'color': 'white', 'margin-bottom': '10px', 'font-size': '22px'}),
                    html.Li('Filter by year.', 
                        style={'color': 'white', 'margin-bottom': '10px', 'font-size': '22px'}),
                    html.Li('Filter according to crime type of interest.', 
                        style={'color': 'white', 'margin-bottom': '10px', 'font-size': '22px'}),
                    html.Li('Compare suburbs/LGA according to their safety!', 
                        style={'color': 'white', 'font-size': '22px'})
                    ], style={
                        'padding': '20px',
                        'list-style-type': 'decimal',
                        'width':'90%',
                        'margin':'0 auto',
                        'overflow':'hidden',
                        'text-align':'left'
                        }
                    )
                ])
            ], style={
                'backgroundColor': CARD_COLOR,
                'border': 'none',
                'borderRadius': '10px',
                'margin': '10px',
                'padding': '20px',
            }),

            dbc.Row([
                html.Div([
                    html.H3("Choose 2 Suburbs (and filter by year)"),
                    html.Div([
                        # Suburb dropdown
                        dcc.Dropdown(
                            id='suburb-dropdown',
                            options=[{'label': lga, 'value': lga} for lga in df['LGA']],
                            clearable=False, 
                            multi=True,
                            value=['Albury','Ballina'],
                            placeholder="Please select 2 suburbs", 
                            style={
                                'width':'100%',
                                'height':'40px',
                                'marginRight': '20px',
                                'font-size': '20px', 
                                'color': 'black',
                            }
                        ),
                        # Year Dropdown
                        dcc.Dropdown(
                            id='year-dropdown',
                            options=years,
                            clearable=True, #original is false
                            value='2023',
                            placeholder="Please select year",
                            style={
                                'width': '100%',
                                'height':'40px',
                                'font-size': '20px', 
                                'color': 'black',
                            }
                        ),
                    ], style={
                        'display':'flex',
                        'gap':'5px',
                        'align-items':'center',
                    }),

                    html.Div(id='warning-message', style={'color': 'red', 'font-weight': 'bold'}),
                    html.Div(
                        html.H4("Filter by crime type")
                        ),
                    # Crime Type Dropdown
                    dcc.Dropdown(
                        id='crime-type-dropdown',
                        options=crime_type,
                        value='Theft',
                        clearable=True,
                        style={
                            'width':'100%',
                            'height':'40px',
                            'marginRight': '20px',
                            'font-size': '20px', 
                            'color':'black'
                        }
                    )
                ])
            ], style={
                'backgroundColor': CARD_COLOR, 
                'border': 'none', 
                'borderRadius': '10px', 
                'margin': '10px', 
                'padding': '20px'}
            ), # End Row - All Filter
                    
                    dbc.Row([  # Top 3 Safest Suburbs
                        html.H3('Top 3 Safest Suburbs', style={'color': TEXT_COLOR}),
                        html.Div(
                            id='top_suburbs',
                            style={
                                'display': 'inline-flex', 
                                'gap': '15px',
                                'white-space': 'nowrap',
                                'overflow': 'hidden',
                                'text-overflow': 'ellipsis',
                                'font-size': '20px',
                                'width': '100%',
                            }
                        ),
                            ], style={
                                'backgroundColor': CARD_COLOR,
                                'border': 'none',
                                'borderRadius': '10px',
                                'margin': '10px',
                                'padding': '20px',
                            }), # End Row - Top 3 Safest suburb
                        

            dbc.Row([ # Heatmap
                html.H3("Crime Heatmap"),
                dcc.Graph(
                    id='choropleth-map', 
                    ),
                #Data source acknowledgement
                html.Div([
                    html.P('Crime data sourced from the NSW Bureau of Crime Statistics and Research (BOCSAR). Data accessed from the publicly-available dataset via BOCSAR Crime Tool',
                        style={
                            'font-style':'italic',
                            'font-size':'20px',
                            'color':'white',
                            'margin':'0px'
                        })
                ]),
            ], style={
                'border':'none', 
                'border-radius': '10px', 
                'margin': '10px',
                'padding': '20px',
                'backgroundColor':CARD_COLOR})
        ], lg=6), # End Left Column


        dbc.Col([ # Right Column
            dbc.Row([ # Safety Score
                html.Div(
                    html.H3("Overall Safety Score")
                ),
                html.Div(
                    id='gauge-output',
                    style={
                        'display': 'flex',
                        'flex-wrap': 'wrap',
                        'gap': '15px',
                        'width': '100%',
                        'justify-content': 'space-evenly'
                    }
                )

            ], style={
                'border':'none', 
                'border-radius': '10px', 
                'margin': '10px',
                'padding': '20px',
                'backgroundColor':CARD_COLOR}), # end safety score
            
            dbc.Row([ # Top Crime Types
                html.Div(
                    html.H3("Top Crime Types")
                ),
                dbc.Col([ # graph 1
                        html.Div(id='top-crime-1-graph')
                ], lg=6),
                dbc.Col([ # graph 2
                        html.Div(id='top-crime-2-graph')
                ], lg=6)
            ], style={
                    'border':'none', 
                    'border-radius': '10px', 
                    'margin': '10px',
                    'padding': '20px',
                    'backgroundColor':CARD_COLOR}
                    ), # End Top Crime

            # 5Y Crime Trend
            dbc.Row([
                html.Div(
                    html.H3("5 Year Crime Trend")
                ),
                html.Div(id='crime-trend-graph')
                
                ], style={
                    'border':'none', 
                    'border-radius': '10px', 
                    'margin': '10px',
                    'padding': '20px',
                    'backgroundColor':CARD_COLOR}
                    ),

            dbc.Row([ # Crime Compared 
                html.Div(
                    html.H3("Crimes Compared")
                ),
                html.Div([
                    dcc.Checklist(
                        id='crime_count',
                        options=crime_type,
                        value=['Theft','Drug'],
                        inline=True,
                        style={
                            'display': 'flex',
                            'justify-content': 'space-around',
                            'align-items': 'center',
                            'width': '100%',
                            'padding': '20px 40px',
                            'margin': '20px 0',
                            'font-size': '18px',
                            'color': 'white'
                        },
                        inputStyle={
                            "margin-right": "10px",
                            "transform": "scale(1.2)" 
            },
                        labelStyle={
                            "margin-right": "40px",
                            "display": "inline-flex",
                            "align-items": "center"
            }
                    ),
                    html.Div(id='crime-compared-graph')
                ])
            ], style={
                'border':'none',
                'border-radius': '10px', 
                'margin': '10px',
                'padding': '20px',
                'backgroundColor':CARD_COLOR})
        ], lg=6) # End Right Column

    ]) # End Big Row

], fluid=True, style={'backgroundColor': BACKGROUND_COLOR}) # End Container

# Callback - Top 3 Safest Suburbs
@app.callback(
    Output('top_suburbs', 'children'),
    Input('year-dropdown', 'value')
)
def update_top_safest_suburbs(selected_year):
    """Update the top 3 safest suburbs based on the selected year."""

    # Top 3 suburbs based on the 'Final_Safety_Score'
    top_suburbs = df.nlargest(3, 'Final_Safety_Score')['LGA']
    
    items = [
        html.Div(f"{suburb}", style={'font-size': '20px', 'margin-bottom': '5px'}) 
        for suburb in top_suburbs
    ]
    return items

# Callback - All Filter
@app.callback(
    [Output('gauge-output', 'children'),
     Output('warning-message', 'children'),
     Output('choropleth-map', 'figure'),
     Output('top-crime-1-graph', 'children'),
     Output('top-crime-2-graph', 'children'),
     Output('crime-trend-graph', 'children'),
     Output('crime-compared-graph', 'children')],
    [Input('suburb-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input('crime-type-dropdown', 'value'),
    Input('crime_count', 'value')]
)
def update_gauge(suburbs,selected_year,selected_crime_type,selected_crime):
    top_crime_1_fig = []
    top_crime_2_fig = []
    if len(suburbs) > 2:
        return [], "Only a maximum of 2 suburbs can be selected.", [], [], [], [], []

    # Heatmap
    if not selected_crime_type:
        selected_crime_type = 'Theft'
    selected_column = f"{selected_crime_type}_Count_{selected_year}"
    
    if selected_column not in data.columns:
        selected_column = f'Theft_Count_{selected_year}'
    
    heat_map= px.choropleth(data,
        geojson=geojson, 
        locations='nsw_loca_2', 
        color=selected_column, 
        featureidkey="properties.nsw_loca_2",
        hover_name='nsw_loca_2',
        hover_data={selected_column: True, 'nsw_loca_2': False},
        labels={selected_column: 'Number of {}'.format(selected_crime_type)},
        range_color=(0, 1000),
        color_continuous_scale="Redor"
    )
    heat_map.update_geos(
        fitbounds=None,
        visible=False,
        projection_scale=600,
        center=dict(lat=-33.85, lon=151.13), # Sydney Coordinates
        )
    heat_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor=CARD_COLOR,
        plot_bgcolor=CARD_COLOR,
        height=1000,
        geo=dict(
            projection_type="mercator",
            bgcolor=CARD_COLOR,
            center=dict(lat=-33.85, lon=151.13),
            projection_scale=600,
            showframe = False
            ),
            coloraxis=dict(
            colorbar=dict(
            title=dict(
                text='Number of {}'.format(selected_crime_type),
                side='right'
                ),
                thickness=20,
                len=0.75,
                x=1.02,
                xanchor='left',
                y=0.5,
                yanchor='middle',
                tickmode='auto',
                nticks=10,
                showticklabels=True,
                tickfont=dict(size=12, color='white'),
                titlefont=dict(size=14, color='white')
            )
        )
    )

    # Safety Score Gauge
    gauges = []
    gauge_style = {
        'flex': '1 1 auto',
        'min-width': '300px',
        'max-width': '400px',
        'height': '300px',
        'padding': '0'
    }

    for suburb in suburbs:
        score = df.loc[df['LGA'] == suburb, 'Final_Safety_Score'].values[0]

        # Gauge Colour Logic
        if score >= 70:
            gauge_color ='#00CC96'
        elif 50<= score < 70:
            gauge_color='#FECB52'
        else:
            gauge_color = '#EF553B'

        gauge = dcc.Graph(
            figure=go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=score,
                    title={
                        'text': f"{suburb}", 
                        'font': {'size': 20, 'color':'white'}
                        },
                    number={
                        'font': {'color': 'white'}
                        },
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1.5, 'tickcolor': "black"},
                        'bar': {'color': gauge_color, 'thickness': 0.3},
                        'borderwidth': 0,
                        'bgcolor': CARD_COLOR
                    }
                )
            ).update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                height=300,
                paper_bgcolor=CARD_COLOR,
                plot_bgcolor=CARD_COLOR
            ),
            style=gauge_style
        )
        gauges.append(gauge)

    # Top Crime Types - Graph 1
    try:
        top_crime_1_data = df[df['LGA'] == suburbs[0]][['LGA', 'Theft_Count_{}'.format(selected_year), 
                                                                'Drug_Count_{}'.format(selected_year), 
                                                                'Assault_Count_{}'.format(selected_year), 
                                                                'Damage_Count_{}'.format(selected_year)]]
        
        top_crime_1_counts = {
            'Theft': top_crime_1_data['Theft_Count_{}'.format(selected_year)].values[0],
            'Drug': top_crime_1_data['Drug_Count_{}'.format(selected_year)].values[0],
            'Assault': top_crime_1_data['Assault_Count_{}'.format(selected_year)].values[0],
            'Damage': top_crime_1_data['Damage_Count_{}'.format(selected_year)].values[0]
        }

        top_crime_1_fig = dcc.Graph(figure=px.pie(
            names=top_crime_1_counts.keys(),
            values=top_crime_1_counts.values(),
            title='{}'.format(suburbs[0]),
            hole=.4
        ).update_traces(textposition='inside').update_layout(
            title_x=0.5,
            uniformtext_minsize=12, 
            uniformtext_mode='hide',
            paper_bgcolor=CARD_COLOR,
            plot_bgcolor=CARD_COLOR,
            title_font=dict(color='white',size=18),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.2,
                xanchor='center',
                x=0.5,
                font=dict(color='white',size=18)
            )))
    except IndexError:
        top_crime_1_fig = []

# Top Crime Types - Graph 2
    try:
        top_crime_2_data = df[df['LGA'] == suburbs[1]][['LGA', 'Theft_Count_{}'.format(selected_year), 
                                                                'Drug_Count_{}'.format(selected_year), 
                                                                'Assault_Count_{}'.format(selected_year), 
                                                                'Damage_Count_{}'.format(selected_year)]]
        
        top_crime_2_counts = {
            'Theft': top_crime_2_data['Theft_Count_{}'.format(selected_year)].values[0],
            'Drug': top_crime_2_data['Drug_Count_{}'.format(selected_year)].values[0],
            'Assault': top_crime_2_data['Assault_Count_{}'.format(selected_year)].values[0],
            'Damage': top_crime_2_data['Damage_Count_{}'.format(selected_year)].values[0]
        }

        top_crime_2_fig = dcc.Graph(figure=px.pie(
        names=top_crime_2_counts.keys(),
        values=top_crime_2_counts.values(),
        title='{}'.format(suburbs[1]),
        hole=.4
        ).update_traces(
            textposition='inside'
        ).update_layout(
            title_x=0.5,
            uniformtext_minsize=12, 
            uniformtext_mode='hide',
            paper_bgcolor=CARD_COLOR,
            plot_bgcolor=CARD_COLOR,
            title_font=dict(color='white',size=18),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.2,
                xanchor='center',
                x=0.5,
                font=dict(color='white', size=18)
            )
        ))
    except IndexError:
        top_crime_2_fig = []


# 5Y Crime Trend
    try:
        suburb1_trend = df[df['LGA'] == suburbs[0]]
        suburb1_trend_rates = [suburb1_trend[f'{selected_crime_type}_Rate_{year}'].values[0] for year in years[:-1]] + [suburb1_trend[f'Predicted_{selected_crime_type}_2025'].values[0]]
            
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=years[1:], y=suburb1_trend_rates[:-1], mode='lines+markers', line=dict(color='#ef43cf', width=4), name=f'{suburbs[0]} - Actual'))
        fig_trend.add_trace(go.Scatter(x=[years[-1],'2025'], y=suburb1_trend_rates[-2:], mode='lines+markers', line=dict(dash='dot', color='#ef43cf', width=4), name=f'{suburbs[0]} - Predicted'))
    except IndexError:
        ret = False

    try:
        suburb2_trend = df[df['LGA'] == suburbs[1]]
        suburb2_trend_rates = [suburb2_trend[f'{selected_crime_type}_Rate_{year}'].values[0] for year in years[:-1]] + [suburb2_trend[f'Predicted_{selected_crime_type}_2025'].values[0]]
    
        fig_trend.add_trace(go.Scatter(x=years[1:], y=suburb2_trend_rates[:-1], mode='lines+markers', line=dict(color='#38b6ff', width=4), name=f'{suburbs[1]} - Actual'))
        fig_trend.add_trace(go.Scatter(x=[years[-1], '2025'], y=suburb2_trend_rates[-2:], mode='lines+markers', line=dict(dash='dot', color='#38b6ff', width=4), name=f'{suburbs[1]} - Predicted'))
    except IndexError:
        ret = False
    
    try:
        fig_trend
    except NameError:
        crime_trend_graph = []
    else:
        fig_trend.update_layout(
title=dict(
            text=f'{selected_crime_type} Rate Trend',
            font=dict(color='white',size=18)
        ),
        xaxis=dict(
            title=dict(text='Year', font=dict(color='white',size=18)),
            tickfont=dict(color='white',size=16),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(text=f'{selected_crime_type} Rate', font=dict(color='white',size=18)),
            tickfont=dict(color='white',size=16),
            showgrid=False
        ),
        legend=dict(
            font=dict(color='white',size=18),
            bgcolor='#353a50',
            bordercolor='white'
        ),
            paper_bgcolor=CARD_COLOR,
            plot_bgcolor=CARD_COLOR

        )
        crime_trend_graph = dcc.Graph(figure=fig_trend)

    # callback for crime compared
    if not selected_crime or not selected_year:
        crime_compare_graph = []
    else:
        fig = go.Figure()

        for crime in selected_crime:
            count_column = '{}_Count_{}'.format(crime, selected_year)

            if count_column in df.columns:
                # Filter data for Suburb 1
                try:
                    crime1_compared_data = df[df['LGA'] == suburbs[0]]
                    crime1_compared_sum = crime1_compared_data[count_column].sum()
                    fig.add_trace(
                        go.Bar(
                            x=[crime],
                            y=[crime1_compared_sum],
                            name= '{}'.format(suburbs[0]),
                            marker=dict(color='#ef43cf', opacity=0.75),
                            offsetgroup=0,
                            marker_line_width=0
                            )
                    )
                except IndexError:
                    del fig
                    break
                
                # Filter data for Suburb 2
                try:
                    crime2_compared_data = df[df['LGA'] == suburbs[1]]
                    crime2_compared_sum = crime2_compared_data[count_column].sum()
                    fig.add_trace(
                        go.Bar(
                            x=[crime],
                            y=[crime2_compared_sum],
                            name= '{}'.format(suburbs[1]),
                            marker=dict(color='#38b6ff', opacity=0.75),
                            offsetgroup=1,
                            marker_line_width=0
                            )
                    )
                except IndexError:
                    ret = False

    try:
        fig
    except NameError:
        crime_compare_graph = []
    else:

        fig.update_layout(
            barmode='group',
            bargap=0.15,
            bargroupgap=0.1,
            xaxis=dict(
                type='category', 
                title='Crime Type',
                title_font=dict(color='white', size=18), 
                tickfont=dict(color='white', size=16),
                showgrid=False,),
            yaxis=dict(
                title='Crime Count',
                title_font=dict(color='white', size=18), 
                tickfont=dict(color='white', size=16),
                showgrid=False,),
            margin=dict(t=10),
            legend=dict(
                font=dict(color='white',size=18),
                bgcolor=CARD_COLOR,
                bordercolor='white'
        ),
            paper_bgcolor=CARD_COLOR,
            plot_bgcolor=CARD_COLOR
        )
        
        fig.update_traces(showlegend=False)
        crime_compare_graph = dcc.Graph(figure=fig)

    return gauges, "", heat_map, top_crime_1_fig, top_crime_2_fig, crime_trend_graph, crime_compare_graph

if __name__ == '__main__':
    app.run(debug=True)
