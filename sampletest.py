import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    html.H1("Remittance Data Dashboard", style={"textAlign": "center"}),

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
    dcc.Graph(id="sunburst")
])

# Callbacks for interactivity
@app.callback(
    [Output("lineplot", "figure"),
     Output("barplot", "figure"),
     Output("sunburst", "figure")],
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

    # Sunburst plot
    sunburst_fig = px.sunburst(
        filtered_data,
        path=["Region/Country", "Month_Year"],
        values="Value",
        title=f"Sunburst of Remittances in {selected_year}",
        labels={"Value": "Remittance (USD)"},
        color="Value",
        color_continuous_scale='RdBu',
        width=800,
        height=700
    )
    sunburst_fig.update_layout(paper_bgcolor='#111111', plot_bgcolor='#111111', font=dict(color='#7FDBFF'))
    sunburst_fig.update_traces(textinfo="label+value+percent entry")

    return line_fig, bar_fig, sunburst_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True) 