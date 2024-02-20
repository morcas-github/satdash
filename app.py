from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import country_converter as coco

cc = coco.CountryConverter()

df = pd.read_csv('sat-db-clean.csv')

# TODO: move source columns omission to clean.py file
df = df.loc[:,~df.columns.str.startswith('Name of Satellite, Alternate Names')]
df = df.loc[:,~df.columns.str.startswith('Source')]
df = df.loc[:,~df.columns.str.startswith('Comments')]
df = df.loc[:,~df.columns.str.startswith('Detailed Purpose')]
df = df.loc[:,~df.columns.str.startswith('Dry Mass')]
df = df.loc[:,~df.columns.str.startswith('Type of Orbit')]
df = df.loc[:,~df.columns.str.startswith('Eccentricity')]
df = df.loc[:,~df.columns.str.startswith('Inclination')]
df = df.loc[:,~df.columns.str.startswith('Power')]
df = df.loc[:,~df.columns.str.startswith('Expected Lifetime')]
df = df.loc[:,~df.columns.str.startswith('Country/Org of UN Registry')]
df['Country of Operator/Owner'] = df['Country of Operator/Owner'].str.strip()


cf = df.groupby(['Country of Operator/Owner']).size().sort_values(ascending=False).reset_index()
cf.rename(columns={0: 'Count'}, inplace=True)

jointOwnedFilter = cf['Country of Operator/Owner'].str.contains("/")

solocf = cf[~jointOwnedFilter]

iso_code = cc.pandas_convert(series=solocf['Country of Operator/Owner'], to='ISO3', not_found=None)

cf['iso_code'] = iso_code

pie = px.pie(cf.head(10), values='Count', names='Country of Operator/Owner')


map = px.choropleth(cf, locations="iso_code",
                    color="Count", # lifeExp is a column of gapminder
                    hover_name="Country of Operator/Owner", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='SatDash', style={'textAlign': 'center'}),
    html.Hr(),
    html.H2('Searchable Satellite Datatable', style={'textAlign': 'center'}),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=20,
        style_table={'overflowX': 'scroll'},
    ),
    html.Div(id='datatable-interactivity-container'),
    html.Hr(),
    html.H2("Satellite Count by Country of Operator/Owner", style={'textAlign': 'center'}),
    dash_table.DataTable(
        id='country-counts-table',
        columns=[
            {"name": "Country of Operator/Owner", "id": "Country of Operator/Owner"},
            {"name": "Count", "id": "Count"}
        ],
        page_current=0,
        page_size=20,
        data=cf.reset_index().to_dict('records')  # Reset index to make 'Country of Operator/Owner' a column
    ),
    html.Hr(),
    html.H2("Hoverable World Map: Satellites per Country", style={'textAlign': 'center'}),
    html.H3("(Jointly Operated/Owned Satellites omitted)", style={'textAlign': 'center'}),
    dcc.Graph(figure=map),
    html.H2("Top 10 Countries with Most Active Satellites", style={'textAlign': 'center'}),
    dcc.Graph(figure=pie)

])


@callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


if __name__ == '__main__':
    app.run(debug=True)
