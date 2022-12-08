import dash
from dash import html, Output, Input, State
from dash import dcc
from dash.exceptions import PreventUpdate
from datetime import datetime
import plotly.graph_objects as go
from dash import dash_table
from dash.dash_table.Format import Group
import pandas as pd

font_awesome = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css"
meta_tags = [{"name": "viewport", "content": "width=device-width"}]
#external_stylesheets = [meta_tags, font_awesome]
external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Roboto&display=swap', meta_tags, font_awesome
]

ELECTRIC_LOGO = "/assets/electric_logo_v2.png"
P_SPARX = "assets/favicon-32x32.png"

electric_cars = pd.read_csv(r'C:\Users\Admin\Desktop\Plotly_Dashboards\Dashboard_ElectricCars\data\electric_cars_V2.csv')
# Date section turned into datetime dtype
electric_cars['Date'] = pd.to_datetime(electric_cars['Date'], format="%d/%m/%Y")

# Format and create Year into a separate column
electric_cars["Year"] = electric_cars['Date'].dt.year

# Format and create Month into a separate column
electric_cars["Months"] = electric_cars['Date'].dt.month_name()

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width"}])


app.layout = html.Div([
        html.Div([
            html.Div([
                html.Img(
                    src=ELECTRIC_LOGO,
                    style={'height': '30px'},
                    className="logo",
                ),
                html.H6('Electric Cars Impact  Dashboard',
                        style={'color':'white'},
                        className='nav_title'),
            ], className="nav_header"),  # Will have to add a Space here with the css to move 'current_time' - to the right
            html.H6(id='current_time',
                    style={'color': 'white'},
                    className="time_position"),

            # Update the time in the dash app
            html.Div([
                dcc.Interval(id='realtime_update',
                             interval=1000,  # updates every second
                             n_intervals=0)
            ]),
            html.A(
                href="https://pandasparx.com/dashboards.html",
                target="_blank",
                children=[
                    html.Img(
                        alt="pandasparX - Dashboards",
                        src=P_SPARX,
                        className="pandasparx_logo",
                    )
                ]
            ),
        ], className="nav_container"), # Holds all the elements of the top nav


        html.Div([
            html.Div([
                html.H3('Electric Cars Sales Insights',
                        style={'color': '#0D160B'})
            ])

        ], id='title'),

        # First Row

        html.Div([
            html.Div([
                html.H3('Electric Cars MultiSpecification Dashboard Insights',
                        style={'color': '#0D160B'})
            ], className='one-third column', id='sub_title1'),

            html.Div([
                html.P('Find Year', className="fix_label", style={'color': '#0D160B'}),
                dcc.Slider(id='year_slider',
                           updatemode='drag',
                           included=False,  # Previous values will not be processed- Figures for the year selected shows
                           tooltip={'always_visible': True},
                           min=2016,
                           max=2022,
                           step=1, #  Shows all the values within the Year by one 2016, 2017 etc - Step=, 2016, 2018 etc
                           dots=False,
                           value=2022,
                           marks={str(yr): str(yr) for yr in range(2016, 2022)},
                           className='dcc_desc'),

            ], className='one-third column', id='heading_title2'),

            # Radio Items
            html.Div([
                html.P('Options', className="fix_label", style={'color': '#0D160B'}),
                dcc.RadioItems(id='radio_items',
                           labelStyle={'display': 'inline-block'},
                           value='low',
                           options=[{'label': i, 'value': i} for i in electric_cars['Mileage Range(km)'].unique()],
                           style={'textAlign': 'center', 'color': '#0D160B'},
                           className='dcc_desc'),

            ], className='one-third column', id='heading_title3'),

        ], id='header', className='row flex-display', style={'marginBottom': '25px'}),

        html.Div([
            html.Div([
                dcc.Graph(id='pie_chart', config={'displayModeBar': 'hover'},
                          style={'height': '350px'}),

            ], className='second_container four columns',
                style={
                'height': '400px',
                'margin-left': '10px'}),

            html.Div([
                dcc.Graph(id='line_chart', config={'displayModeBar': 'hover'},
                          style={'height': '350px'}),

            ], className='second_container four columns',
                style={
                'height': '400px',
                'margin-left': '10px'}),

            html.Div([
                dcc.Graph(id='stacked_chart', config={'displayModeBar': 'hover'},
                          style={'height': '350px'}),

            ], className='second_container four columns',
                style={
                'height': '400px',
                'margin-left': '10px'}),


        ], className='row flex-display'),

        html.Div([
            html.Div([
                dash_table.DataTable(id='data_table',
                                     columns=[{'id': i, 'name': i} for i in
                                              electric_cars.loc[:, ['Date', 'Year', 'E-Type', 'Months', 'BodyType', 'Title',
                                                                    'Mileage Range(km)', 'topspeed_km/h', 'range_km',
                                                                    'fastcharge_speed_km/h', 'price_de_euro',
                                                                    'price_nl_euro', 'price_uk_pound',
                                                                    'Sales']]],
                                     # Virtualization helps the datatable to fit directly into the outline box
                                     virtualization=True,
                                     # Text/ Strings Aligned to the left - int aligned to the right
                                     style_cell_conditional=[
                                         {
                                             'if': {'column_id': i},
                                             'textAlign': 'left'
                                         } for i in ['Date', 'Year', 'Months', 'BodyType', 'Title','Mileage Range(km)',
                                                     'E-Type']

                                     ],
                                     style_cell={
                                                 'padding': '5px',
                                                 'min-width': '100px',
                                                 'backgroundColor': '#E7E7E7',
                                                 'color': '#1f2c56',
                                                 'border-bottom': '0.01rem solid #19AAE1'},
                                     style_header={
                                         'backgroundColor': '#8a8888',
                                         'fontWeight': 'bold',
                                         'font': 'sans-serif',
                                         'color': '#fff',
                                         'border': '3px solid #FA824C'
                                     },
                                     style_table={'min-height': '400px', 'overflowY': 'auto'},
                                     # This will take out the vertical grid lines
                                     style_as_list_view=True,
                                     #style_data={'styleOverflow': 'hidden', 'color': 'white'},
                                     fixed_rows={'headers': True}, # Sticky Header
                                     page_action='native',
                                     page_size=10,
                                     sort_mode='multi',
                                     sort_action='native'
                                     ),
            ], className='second_container four columns',
                style={
                'max-height': '400px',
                'margin-left': '10px'}),

            html.Div([
                dcc.RadioItems(id='second_radio',
                               labelStyle={'display': 'inline-block'},
                               value='E-Type',
                               options=[{'label': 'E-Type', 'value': 'E-Type'},
                                        {'label': 'BodyType', 'value': 'BodyType'}],
                               style={'text-align': 'center', 'color': 'white'},
                               className='dcc_comp'),

                dcc.Graph(id='barchart', config={'displayModeBar': 'hover'},
                          style={'height': '350px'})

            ], className='second_container six columns',
                style={
                'height': '400px',
                'margin-left': '10px'}),

            html.Div([
                html.H3('Interactive Digital Board',
                       style={
                           'textAlign': 'center',
                           'color': '#Fa824c',
                       }),
                html.Div(id='digital_board'),
                html.Div(id='digital_board_pre'),
                html.Div(id='digital_board_gro'),

            ], className='second_container two columns',
                style={
                'height': '400px',
                'margin-left': '10px'}
            ),

        ], className='row flex-display'),

        html.Div([
                html.Footer('Electric Cars Dashboard',
                            className='footer_content')

        ], id='footer')


], id='mainContainer')

# CALL BACKS

# Time in Navbar
@app.callback(Output('current_time', 'children'),
            [Input('realtime_update', 'n_intervals')])
def time_update(n_intervals):
    if n_intervals == 0:
        raise PreventUpdate
    else:
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y | %H: %M: %S")

    return[
        html.Div(dt_string)
    ]


# Pie/Donut Chart

@app.callback(Output('pie_chart', 'figure'),
              [Input('year_slider', 'value')],
              [Input('radio_items', 'value')])
def pie_chart(year_slider, radio_items):
    pie_electric = electric_cars.groupby(['Year', 'Mileage Range(km)', 'BodyType'])['Sales'].sum().reset_index()
    pie_pass_van = pie_electric[(pie_electric['Year'] == year_slider) & (pie_electric['Mileage Range(km)'] == radio_items) & (pie_electric['BodyType'] == 'Passenger Van')]['Sales'].sum()
    pie_cab = pie_electric[(pie_electric['Year'] == year_slider) & (pie_electric['Mileage Range(km)'] == radio_items) & (pie_electric['BodyType'] == 'Cabriolet')]['Sales'].sum()
    pie_hatchback = pie_electric[(pie_electric['Year'] == year_slider) & (pie_electric['Mileage Range(km)'] == radio_items) & (pie_electric['BodyType'] == 'HatchBack')]['Sales'].sum()
    pie_estate = pie_electric[(pie_electric['Year'] == year_slider) & (pie_electric['Mileage Range(km)'] == radio_items) & (pie_electric['BodyType'] == 'Estate')]['Sales'].sum()
    pie_roadster = pie_electric[(pie_electric['Year'] == year_slider) & (pie_electric['Mileage Range(km)'] == radio_items) & (pie_electric['BodyType'] == 'Roadster')]['Sales'].sum()
    pie_saloon = pie_electric[(pie_electric['Year'] == year_slider) & (pie_electric['Mileage Range(km)'] == radio_items) & (pie_electric['BodyType'] == 'Saloon')]['Sales'].sum()
    pie_suv = pie_electric[(pie_electric['Year'] == year_slider) & (pie_electric['Mileage Range(km)'] == radio_items) & (pie_electric['BodyType'] == 'SUV')]['Sales'].sum()
    colors = ['#d0e0e3', '#1F2C56', '#FA824C', '#840032', '#19AAE1', '#666666', '#0000ff', '#e6b8af']

    return {
        'data': [go.Pie(
            labels=['Passenger Van', 'Cabriolet', 'Hatchback', 'Estate', 'Roadster', 'Saloon', 'SUV'],
            values=[pie_pass_van, pie_cab, pie_hatchback, pie_estate, pie_roadster, pie_saloon, pie_suv],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='percent+label',
            texttemplate='%{label} <br>%{value:,.2f}',
            textposition='inside',
            textfont=dict(size=13),
            hole=.3,
            rotation=160,
        )],

        'layout': go.Layout(
            title={'text': '<b>Sales by Body Type selected by Year</b>' + ' ' + str((year_slider)),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': '#1f2c56',
                       'size': 15},
            font=dict(family='Roboto',
                      color='#1f2c56',
                      size=12),
            hovermode='closest',
            margin=dict(l=10, r=10, t=60, b=0),
            paper_bgcolor='#E7E7E7',
            plot_bgcolor='#E7E7E7',
            legend={'orientation': 'h',
                    'bgcolor': '#E7E7E7',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7}
        )
    }

# Line Chart Callback

@app.callback(Output('line_chart','figure'),
              [Input('year_slider','value')],
              [Input('radio_items','value')])
def update_chart(year_slider, radio_items):
    month_sales = electric_cars.groupby(['Year', 'Months', 'Mileage Range(km)'])['Sales'].sum().reset_index()
    update_sales = month_sales[(month_sales['Year'] == year_slider) & (month_sales['Mileage Range(km)'] == radio_items)]

    return {
        'data': [
            go.Scatter(
                x=update_sales['Months'],
                y=update_sales['Sales'],
                text=update_sales['Sales'],
                texttemplate='£' + '%{text:,.2s}',
                mode='markers+lines+text',
                textposition='bottom left',
                line=dict(width=3, color='#FA824C'),
                marker=dict(color='#840032', size=8, symbol='circle',
                            line=dict(color='#840032', width=2)),
                hoverinfo='text',
                hovertext=
                '<b>Year</b>: ' + update_sales['Year'].astype(str) + '<br>' +
                '<b>Months</b>: ' + update_sales['Months'].astype(str) + '<br>' +
                '<b>Mileage Range</b>: ' + update_sales['Mileage Range(km)'].astype(str) + '<br>' +
                '<b>Sales</b>: £' + [f'{x:,.0f}' for x in update_sales['Sales']] + '<br>'
            ),
        ],

        'layout': go.Layout(
            title={'text': '<b>Sales by Year</b>' + ' ' + str((year_slider)),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': '#1F2C56',
                       'size': 15},
            font=dict(family='Roboto',
                      color='#1F2C56',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#E7E7E7',
            plot_bgcolor='#E7E7E7',
            legend={'orientation': 'h',
                    'bgcolor': '#010915',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(t=20, l=0, r=0, b=30),
            xaxis=dict(title='<b></b>',
                       color='#1F2C56',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='#1F2C56',
                       linewidth=2,
                       ticks='outside',
                       tickfont=dict(
                           family='Roboto',
                           color='#1F2C56',
                           size=12
                       )),
            yaxis=dict(title='<b></b>',
                       color='orange',
                       showline=False,
                       showgrid=True,
                       showticklabels=False,
                       linecolor='orange',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Roboto',
                           color='orange',
                           size=12
                       )
                       )

        )
    }

# Stacked Barchart
@app.callback(Output('stacked_chart','figure'),
              [Input('year_slider','value')],
              [Input('radio_items','value')])
def stacked_chart(year_slider, radio_items):
    stacked_sales = electric_cars.groupby(['Year', 'Months', 'Mileage Range(km)'])[['price_uk_pound',
                                                                                    'price_de_euro',
                                                                                    'price_nl_euro']].sum().reset_index()
    # Filtered Dataframe to be used::
    dff2 = stacked_sales[(stacked_sales['Year'] == year_slider) & (stacked_sales['Mileage Range(km)'] == radio_items)]

    return {
        'data': [go.Bar(
                x=dff2['Months'],
                y=dff2['price_uk_pound'],
                text=dff2['price_uk_pound'],
                texttemplate='£%{text:,.0f}',
                textposition='auto',
                name='Price in UK Pound',
                marker=dict(color='#0000ff'),
                hoverinfo='text',
                hovertext=
                '<b>Mileage Range</b>: ' + dff2['Mileage Range(km)'].astype(str) + '<br>' +
                '<b>Year</b>: ' + dff2['Year'].astype(str) + '<br>'
            ),

            go.Bar(
                x=dff2['Months'],
                y=dff2['price_de_euro'],
                text=dff2['price_de_euro'],
                texttemplate='€%{text:,.0f}',
                textposition='auto',
                name='Price in German Euro',
                marker=dict(color='#19AAE1'),
                hoverinfo='text',
                hovertext=
                '<b>Mileage Range</b>: ' + dff2['Mileage Range(km)'].astype(str) + '<br>' +
                '<b>Year</b>: ' + dff2['Year'].astype(str) + '<br>'
            ),

            go.Bar(
                x=dff2['Months'],
                y=dff2['price_nl_euro'],
                text=dff2['price_nl_euro'],
                texttemplate='€%{text:,.0f}',
                textposition='auto',
                name='Price in Netherlands Euro',
                marker=dict(color='#840032'),
                hoverinfo='text',
                hovertext =
                '<b>Mileage Range</b>: ' + dff2['Mileage Range(km)'].astype(str) + '<br>' +
                '<b>Year</b>: ' + dff2['Year'].astype(str) + '<br>',
            ),

        ],

        'layout': go.Layout(
            barmode='stack',
            title={'text': '<b>Total Insights of Car Price range in Europe by Year</b>' + ' ' + str((year_slider)),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': '#1f2c56',
                       'size': 16},
            font=dict(family='sans-serif',
                      color='#1f2c56',
                      size=12),
            hovermode='closest',
             paper_bgcolor='#E7E7E7',
             plot_bgcolor='#E7E7E7',
            legend={'orientation': 'h',
                    'bgcolor': '#E7E7E7',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.2},
            margin=dict(b=1, r=0),
            xaxis=dict(title='<b></b>',
                       tick0=0,
                       dtick=1,
                       color='#1f2c56',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='#1f2c56',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Roboto',
                           color='#1f2c56',
                           size=12
                       )),
            yaxis=dict(title="<b>Sales</b>",
                       color='#1f2c56',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='#1f2c56',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Roboto',
                           color='#1f2c56',
                           size=12
                       ))
        )
    }

# Datatable
@app.callback(Output('data_table','data'),
              [Input('year_slider','value')],
              [Input('radio_items', 'value')])
def datatable_update(year_slider, radio_items):
    datatable = electric_cars[(electric_cars['Year'] == year_slider) & (electric_cars['Mileage Range(km)'] == radio_items)]

    return datatable.to_dict('records')

# Barchart
# id second_radio
# barchart

@app.callback(Output('barchart', 'figure'),
              [Input('year_slider', 'value')],
              [Input('radio_items', 'value')],
              [Input('second_radio', 'value')])
def update_barchart(year_slider, radio_items, second_radio):
    bar_e_type = electric_cars.groupby(['Year', 'E-Type', 'Mileage Range(km)'])['Sales'].sum().reset_index()
    bar_type_process = bar_e_type[(bar_e_type['Year'] == year_slider) & (bar_e_type['Mileage Range(km)'] == radio_items)].sort_values(by=['Sales'], ascending=False).nlargest(10, columns=['Sales'])
    bar_body = electric_cars.groupby(['Year', 'BodyType', 'Mileage Range(km)'])['Sales'].sum().reset_index()
    bar_body_process = bar_body[(bar_body['Year'] == year_slider) & (bar_body['Mileage Range(km)'] == radio_items)].sort_values(by=['Sales'], ascending=False).nlargest(10, columns=['Sales'])

    if second_radio == "E-Type":

        return {
            'data': [
                go.Bar(
                    x=bar_type_process['Sales'],
                    y=bar_type_process['E-Type'],
                    text=bar_type_process['Sales'],
                    texttemplate=' ' +'%{text:,.2s}',
                    textposition='auto',
                    orientation='h',
                    marker=dict(color='#19AAE1'),
                    hoverinfo='text',
                    hovertext=
                    '<b>Year</b>: ' + bar_type_process['Year'].astype(str) + '<br>' +
                    '<b>Make</b>: ' + bar_type_process['E-Type'].astype(str) + '<br>' +
                    '<b>Mileage Range</b>: ' + bar_type_process['Mileage Range(km)'].astype(str) + '<br>' +
                    '<b>Sales</b>: ' + bar_type_process['Sales'].astype(str) + '<br>'

                ),
            ],


            'layout': go.Layout(
                title={'text': '<b>Units Sold in</b>' + ' ' + str((year_slider)),
                       'y': 0.99,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                titlefont={'color': '#1f2c56',
                           'size': 15},
                font=dict(family='Roboto',
                          color='white',
                          size=15),
                hovermode='closest',
                paper_bgcolor='#E7E7E7',
                plot_bgcolor='#E7E7E7',
                legend={'orientation': 'h',
                        'bgcolor': '#010915',
                        'xanchor': 'center', 'x': 0.5, 'y': -0.7},
                margin=dict(t=60, r=0),
                xaxis=dict(title='<b></b>',
                           color='#1f2c56',
                           showline=True,
                           showgrid=True,
                           showticklabels=True,
                           linecolor='#1f2c56',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Roboto',
                               color='#1f2c56',
                               size=12
                           )),
                yaxis=dict(title='<b></b>',
                           color='#1f2c56',
                           autorange='reversed',
                           showline=False,
                           showgrid=False,
                           showticklabels=True,
                           linecolor='#1f2c56',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Roboto',
                               color='#1f2c56',
                               size=12
                           )
                           )
            )
        }

    elif second_radio == 'BodyType':

        return {
            'data': [
                go.Bar(
                    x=bar_body_process['Sales'],
                    y=bar_body_process['BodyType'],
                    text=bar_body_process['Sales'],
                    texttemplate=' ' + '%{text:,.2s}',
                    textposition='auto',
                    orientation='h',
                    marker=dict(color='#19AAE1'),
                    hoverinfo='text',
                    hovertext=
                    '<b>Year</b>: ' + bar_body_process['Year'].astype(str) + '<br>' +
                    '<b>Make</b>: ' + bar_body_process['BodyType'].astype(str) + '<br>' +
                    '<b>Mileage Range</b> ' + bar_body_process['Mileage Range(km)'].astype(str) + '<br>'  # +
                    # '<b>Sales</b>: + [f'{x:,.0s}' for x in bar_make_process['Sales]] + '<br>'
                ),
            ],

            'layout': go.Layout(
                title={'text': '<b>Body Type total unit sales in</b>' + ' ' + str((year_slider)),
                       'y': 0.99,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                titlefont={'color': '#1f2c56',
                           'size': 15},
                font=dict(family='Roboto',
                          color='#1f2c56',
                          size=15),
                hovermode='closest',
                paper_bgcolor='#E7E7E7',
                plot_bgcolor='#E7E7E7',
                legend={'orientation': 'h',
                       'bgcolor': '#010915',
                       'xanchor': 'center', 'x': 0.5, 'y': -0.7},
                margin=dict(t=40, r=0),
                xaxis=dict(title='<b></b>',
                           color='#1f2c56',
                           showline=True,
                           showgrid=True,
                           showticklabels=True,
                           linecolor='#1f2c56',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Roboto',
                               color='#1f2c56',
                               size=12
                           )),
                yaxis=dict(title='<b></b>',
                           color='#1f2c56',
                           autorange='reversed',
                           showline=False,
                           showgrid=False,
                           showticklabels=True,
                           linecolor='#1f2c56',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Roboto',
                               color='#1f2c56',
                               size=12
                           )
                           )

            )
        }



# Digital Board

@app.callback(Output('digital_board','children'),
              [Input('year_slider','value')],
              [Input('radio_items', 'value')])
def digital_board_update(year_slider, radio_items):
    digital_board = electric_cars.groupby(['Year', 'Mileage Range(km)'])['Sales'].sum().reset_index()
    # Filter DataFrame for interactivity year_slider and radio_items
    d_board = digital_board[(digital_board['Year'] == year_slider) & (digital_board
                                                                      ['Mileage Range(km)'] == radio_items)]['Sales'].sum()

    return [
        html.H6(children='Current Year Global Sales Update',
                style={'textAlign': 'center',
                       'color': 'white'}),
        html.P('{0:,.2f}'.format(d_board),
                style={'textAlign': 'center',
                       'color': '#19AAE1',
                       'fontSize': 13,
                       'margin-top': '-10px'}
               )
    ]

# Digital Board_pre
@app.callback(Output('digital_board_pre','children'),
              [Input('year_slider','value')],
              [Input('radio_items', 'value')])
def digital_board_update_1(year_slider, radio_items):
    # Previous Year Global Update
    digital_board_pre = electric_cars.groupby(['Year', 'Mileage Range(km)'])['Sales'].sum().reset_index()
    digital_board_pre['Previous_Year'] = digital_board_pre['Sales'].shift(1)
    # Filter DataFrame for interactivity year_slider and radio_items
    d_board_pre = digital_board_pre[(digital_board_pre['Year'] == year_slider) & (digital_board_pre
                                                                      ['Mileage Range(km)'] == radio_items)]['Previous_Year'].sum()
    return [
        html.H6(children='Previous Year Global Update',
                style={'textAlign': 'center',
                       'color': 'white'}),
        html.P('{0:,.2f}'.format(d_board_pre),
                style={'textAlign': 'center',
                       'color': '#19AAE1',
                       'fontSize': 13,
                       'margin-top': '-10px'}
               )
    ]

# Digital Board_gro
@app.callback(Output('digital_board_gro','children'),
              [Input('year_slider','value')],
              [Input('radio_items', 'value')])
def digital_board_update_2(year_slider, radio_items):
    # Previous Year Global Update
    digital_board_gro = electric_cars.groupby(['Year', 'Mileage Range(km)'])['Sales'].sum().reset_index()
    digital_board_gro['Yearly_Gro'] = digital_board_gro['Sales'].pct_change()
    digital_board_gro['Yearly_Gro'] = digital_board_gro['Yearly_Gro'] * 100
    # Filter DataFrame for interactivity year_slider and radio_items
    d_board_gro = digital_board_gro[(digital_board_gro['Year'] == year_slider) & (digital_board_gro
                                                                      ['Mileage Range(km)'] == radio_items)]['Yearly_Gro'].sum()
    return [
        html.H6(children='Yearly Growth Update',
                style={'textAlign': 'center',
                       'color': 'white'}),
        html.P('{0:,.2f}%'.format(d_board_gro),
                style={'textAlign': 'center',
                       'color': '#19AAE1',
                       'fontSize': 13,
                       'margin-top': '-10px'}
               )
    ]





if __name__ == "__main__":
    app.run(debug=True)