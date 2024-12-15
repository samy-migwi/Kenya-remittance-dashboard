import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load the dataset
df = pd.read_csv(r"C:\Users\Qwon\Desktop\Dev\linkedin_projects\remitances\clsep.csv")

# Melt the DataFrame for easier plotting
df_melted = df.melt(id_vars="Region/Country", var_name="Month_Year", value_name="Value")
df_melted['Year'] = df_melted['Month_Year'].str.extract(r'_(\d{2})$').astype(int) + 2000

# Initialize the Dash app
app = Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1(" Kenya Remittance Data Dashboard  (‘000 USD Equivalent)", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id="year-dropdown",
            options=[{"label": year, "value": year} for year in sorted(df_melted['Year'].unique())],
            value=sorted(df_melted['Year'].unique())[0],
            clearable=False
        )
    ], style={"width": "50%", "margin": "0 auto"}),

    dcc.Graph(id="lineplot"),
    dcc.Graph(id="barplot"),

    html.Div([
        dcc.Graph(id="sunburst1", style={"display": "inline-block", "width": "48%"}),
        dcc.Graph(id="sunburst2", style={"display": "inline-block", "width": "48%"})
    ], style={"display": "flex", "justify-content": "space-between"}),

    dcc.Graph(id="choropleth"),
    # Updated Footer with Detailed Data Handling Information
html.Div([
    html.P(
        "This dashboard is a result of my passion for data analysis and visualization. "
        "I am Samy Migwi, a data scientist who loves working with data to uncover insights."
    ),
    html.P(
        "Data source: ",
        style={"display": "inline-block"}
    ),
    html.A(
        "Central Bank of Kenya",
        href="https://www.centralbank.go.ke/diaspora-remittances/",
        target="_blank",
        style={"color": "#007BFF", "textDecoration": "none", "display": "inline-block"}
    ),
    html.P(
        ". For this analysis, some data was missing and this is how i handled them:",
        style={"marginTop": "10px"}
    ),
    html.Ul([
        html.Li("Bahamas (April 2020): Used NOCB (Next Observation Carried Backward)."),
        html.Li("Iraq (May 2021): Applied LOCF (Last Observation Carried Forward)."),
        html.Li("Iraq (June 2021): Used NOCB."),
        html.Li("China (April 2021): Replaced missing value with the mean calculated using a six-month window (six months before and after).")
    ], style={"textAlign": "left", "marginLeft": "20px"}),

    html.P(
        "The choice of these methods ensured consistency with the monotonic trends observed in the data."
    )
], style={"textAlign": "center", "marginTop": "20px"}),

html.Footer(
    "Developed by Samy Migwi. © 2024 All rights reserved.",
    style={
        "textAlign": "center",
        "padding": "10px",
        "backgroundColor": "#111111",
        "color": "#7FDBFF",
        "marginTop": "20px"
    }
)

    


])

# Callbacks for interactivity
@app.callback(
    [Output("lineplot", "figure"),
     Output("barplot", "figure"),
     Output("sunburst1", "figure"),
     Output("sunburst2", "figure"),
     Output("choropleth", "figure")],
    [Input("year-dropdown", "value")]
)
def update_dashboard(selected_year):
    # Filter data by year
    filtered_data = df_melted[df_melted['Year'] == selected_year]

    # Top 10 countries for line plot
    top_countries = (filtered_data.groupby("Region/Country")['Value'].sum()
                     .nlargest(10).index)
    top_data = filtered_data[filtered_data['Region/Country'].isin(top_countries)]

    # Line plot
    line_fig = px.line(
        top_data,
        x="Month_Year",
        y="Value",
        color="Region/Country",
        title=f"Top 10 Countries by Remittance in {selected_year}",
        labels={"Value": "Remittance (USD)", "Month_Year": "Month"},
        height=800
    )

    # Horizontal bar plot
    bar_data = filtered_data.groupby("Region/Country")['Value'].sum().sort_values(ascending=False)
    bar_fig = px.bar(
        x=bar_data.values,
        y=bar_data.index,
        orientation='h',
        color=bar_data.values,
        color_continuous_scale='RdBu',
        title=f"Total Remittances by Country in {selected_year}",
        labels={"x": "Remittance (USD)", "y": "Country"},
        height=800
    )

    # Sunburst plot 1
    sunburst_fig1 = px.sunburst(
        filtered_data,
        path=["Region/Country", "Month_Year"],
        values="Value",
        title=f"Detailed Sunburst Chart for countries {selected_year}",
        labels={"Value": "Remittance (USD)"},
        color="Value",
        color_continuous_scale='RdBu',
        width=800,
        height=800
    )
    sunburst_fig1.update_traces(textinfo="label+value+percent entry")

    # Sunburst plot 2
    sunburst_fig2 = px.sunburst(
        filtered_data.sort_values(by="Month_Year"),
        path=["Year", "Month_Year", "Region/Country"],
        values="Value",
        title=f"Total Remittances by months in {selected_year}",
        labels={"Value": "Remittance (USD)"},
        color="Value",
        color_continuous_scale='RdBu',
        width=800,
        height=800
    )
    sunburst_fig2.update_traces(textinfo="label+value+percent entry")

    # Choropleth map
    choropleth_data = filtered_data.groupby("Region/Country")["Value"].sum().reset_index()
    choropleth_fig = px.choropleth(
        choropleth_data,
        locations="Region/Country",
        locationmode="country names",
        color="Value",
        hover_data=["Value"],
        title=f"Choropleth Map of Remittances sources in {selected_year}",
        color_continuous_scale="rainbow",
        height=800
    )
    choropleth_fig.update_layout(
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font=dict(color="#7FDBFF")
    )

    return line_fig, bar_fig, sunburst_fig1, sunburst_fig2, choropleth_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
