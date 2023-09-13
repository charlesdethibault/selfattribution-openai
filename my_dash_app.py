# to run : python my_dash_app.py


import dash
from dash import Dash, dcc, html, Input, Output


app = dash.Dash(__name__)


app.layout = html.Div([
   html.H1("My First Dash App"),
   dcc.Graph(
       id='example-graph',
       figure={
           'data': [
               {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'A'},
               {'x': [1, 2, 3], 'y': [2, 4, 3], 'type': 'bar', 'name': 'B'},
           ],
           'layout': {
               'title': 'Sample Bar Chart'
           }
       }
   ),
   dcc.Input(id='input-box', type='text', value=''),
   html.Div(id='output-div')
])


@app.callback(
   Output('output-div', 'children'),
   Input('input-box', 'value')
)
def update_output(value):
   return f'You entered: {value}'


if __name__ == '__main__':
   app.run_server(debug=True)


# I changed sonething to see
