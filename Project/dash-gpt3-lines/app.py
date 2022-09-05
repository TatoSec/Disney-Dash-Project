import os
import secrets
from textwrap import dedent
from turtle import left
from secret_token import api_token

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dash import no_update
from dash.dependencies import Input, Output, State
import plotly.express as px
import openai
import pandas as pd

def Header(name, app):
    title = html.H1(name, style={"margin-top": 5})
    logo = html.Img(
        src=app.get_asset_url("Disney-Logo.png"), style={"float": "right", "height":100,}
    )
    return dbc.Row([dbc.Col(title, md=8), dbc.Col(logo, md=4)])


df = pd.read_csv('disney_data.csv')

# Authentication
openai.api_key = os.getenv(api_token)
openai.api_key = api_token



# Define the prompt
prompt = """


**Code**: ```px.line(df.query("continent == 'Oceania'"), x='year', y='lifeExp', color='country', log_y=False, log_x=False)```
"""

# Create
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

content_style = {"height": "475px"}

chat_input = dbc.InputGroup(
    [
        dbc.Input(
            id="input-text", placeholder="What Disney movie data may I provide ?"
        ),
        dbc.InputGroupAddon(
            dbc.Button("Submit", id="button-submit", color="primary"),
            addon_type="append",
        ),
    ]
)
output_graph = [
    dbc.CardHeader("Disney Data Graph [Domestic Only]"),
    dbc.CardBody(dbc.Spinner(dcc.Graph(id="output-graph", style={"height": "425px"}))),
]
output_code = [
    dbc.CardHeader("Conversation Interface"),
    dbc.CardBody(
        dbc.Spinner(dcc.Markdown("", id="conversation-interface")),
        style={"height": "725px"},
    ),
]

explanation = f"""
*GPT-3 can generate Plotly graphs from a simple description of what you want, and it
can even modify what you have previously generated!
We only needed to load the DisneyData.csv dataset and give the following prompt to GPT-3:*

{prompt}
"""
explanation_card = [
    dbc.CardHeader("What am I looking at?"),
    dbc.CardBody(dcc.Markdown(explanation)),
]

left_col = [dbc.Card(output_graph), html.Br(), dbc.Card(explanation_card)]

right_col = [dbc.Card(output_code), html.Br(), chat_input]

app.layout = dbc.Container(
    [
        Header("Top Grossing Disney Movie", app),
        html.Hr(),
        dbc.Row([dbc.Col(left_col, md=7), dbc.Col(right_col, md=5)]),
    ],
    fluid=True,
)


@app.callback(
    [
        Output("output-graph", "figure"),
        Output("conversation-interface", "children"),
        Output("input-text", "value"),
    ],
    [Input("button-submit", "n_clicks"), Input("input-text", "n_submit")],
    [State("input-text", "value"), State("conversation-interface", "children")],
)
def generate_graph(n_clicks, n_submit, text, conversation):
    if n_clicks is None and n_submit is None:
        default_fig = px.line(
            df.query("genre == 'Action'"),
            x="genre",
            y="total_gross",
            color="_movie_title_",
            log_y=False,
            log_x=False,
        )
        return default_fig, dash.no_update, dash.no_update

    conversation += dedent(
        f"""
    **Description**: {text}

    **Code**:"""
    )

    gpt_input = (prompt + conversation).replace("```", "").replace("**", "")
    print(gpt_input)
    print("-" * 40)

    response = openai.Completion.create(
        engine="davinci",
        prompt=gpt_input,
        max_tokens=200,
        stop=["Description:", "Code:"],
        temperature=0,
        top_p=1,
        n=1,
    )

    output = response.choices[0].text.strip()

    conversation += f" ```{output}```\n"

    try:
        fig = eval(output)
    except Exception as e:
        fig = px.line(title=f"Exception: {e}. Please try again!")

    return fig, conversation, ""


if __name__ == "__main__":
    app.run_server(debug=True)
