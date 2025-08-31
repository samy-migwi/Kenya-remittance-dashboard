import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# Load datasets
df=pd.read_csv(r"C:\Users\KMC\Desktop\ds\remitances\Kenya-remittance-dashboard\data\processed\apr25.csv")
dt=pd.read_csv(r"C:\Users\KMC\Desktop\ds\remitances\Kenya-remittance-dashboard\data\processed\region_apr25.csv")

# Data preprocessing
df_melted = df.melt(id_vars="Region/Country", var_name="Month_Year", value_name="Value")
df_melted['Year'] = df_melted['Month_Year'].str.extract(r'_(\d{2})$').astype(int) + 2000
df_melted['Month'] = df_melted['Month_Year'].str.extract(r'^([A-Za-z]{3})')

# Kenya theme colors
KENYA_THEME = {
    "primary": "#007336",  # Green
    "secondary": "#BB0000",  # Red
    "dark": "#000000",      # Black
    "light": "#FFFFFF",     # White
    "accent": "#FFC72C",    # Yellow (for highlights)
}

# Initialize the Dash app with Bootstrap and custom theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Load Bootstrap template for Plotly figures
load_figure_template("bootstrap")

# Custom CSS styles
CUSTOM_STYLES = {
    "header": {
        "background": f"linear-gradient(135deg, {KENYA_THEME['primary']} 0%, {KENYA_THEME['secondary']} 100%)",
        "color": KENYA_THEME["light"],
        "padding": "1.5rem",
        "borderRadius": "0.5rem",
        "marginBottom": "2rem",
        "boxShadow": "0 4px 6px rgba(0,0,0,0.1)"
    },
    "card": {
        "border": f"1px solid {KENYA_THEME['primary']}",
        "borderRadius": "0.5rem",
        "padding": "1rem",
        "marginBottom": "1.5rem",
        "boxShadow": "0 2px 4px rgba(0,0,0,0.05)"
    },
    "dropdown": {
        "marginBottom": "1.5rem"
    },
    "graph-container": {
        "borderRadius": "0.5rem",
        "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
        "padding": "1rem",
        "backgroundColor": KENYA_THEME["light"]
    }
}

def create_total_indicator(current_month="Jan_23"):
    current_total = dt[current_month].sum()
    
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number",
        value=current_total,
        number={
            "prefix": "<span style='font-size:0.6em; color:" + KENYA_THEME["dark"] + "'>$</span>",
            "valueformat": ",",
            "font": {"size": 48, "family": "Arial", "color": KENYA_THEME["dark"]},
        },
        title={
            "text": f"<b>TOTAL REMITTANCES ({current_month.replace('_', ' ').upper()})</b>",
            "font": {"size": 20, "family": "Arial", "color": KENYA_THEME["secondary"]},
            "align": "center"
        },
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    
    fig.update_layout(
        plot_bgcolor=KENYA_THEME["light"],
        paper_bgcolor=KENYA_THEME["light"],
        margin=dict(l=20, r=20, t=60, b=20),
        height=180
    )
    
    return fig

def create_change_indicator(current_month="Jan_23", comparison_type="month"):
    month_columns = [col for col in dt.columns if col != 'Region/Country']
    
    if comparison_type == "month":
        current_index = month_columns.index(current_month)
        previous_month = month_columns[current_index - 1] if current_index > 0 else None
        if not previous_month:
            return go.Figure()
        
        current_total = dt[current_month].sum()
        previous_total = dt[previous_month].sum()
        difference = current_total - previous_total
        pct_change = (difference / previous_total * 100) if previous_total else 0
        title = f"MONTHLY CHANGE FROM {previous_month.replace('_', ' ').upper()}"
        current_label = f"{current_month.replace('_', ' ').upper()} TOTAL"
        previous_label = f"{previous_month.replace('_', ' ').upper()} TOTAL"
        
    else:  # year-over-year
        month_name, year_suffix = current_month.split("_")
        previous_year = f"{month_name}_{int(year_suffix) - 1:02d}"
        
        if previous_year not in month_columns:
            return go.Figure()
        
        current_total = dt[current_month].sum()
        previous_total = dt[previous_year].sum()
        difference = current_total - previous_total
        pct_change = (difference / previous_total * 100) if previous_total else 0
        title = f"YEARLY CHANGE FROM {previous_year.replace('_', ' ').upper()}"
        current_label = f"{current_month.replace('_', ' ').upper()} TOTAL"
        previous_label = f"{previous_year.replace('_', ' ').upper()} TOTAL"
    
    change_color = KENYA_THEME["primary"] if difference >= 0 else KENYA_THEME["secondary"]
    change_direction = "▲" if difference >= 0 else "▼"
    
    fig = go.Figure()
    
    # Main change indicator
    fig.add_trace(go.Indicator(
        mode="number",
        value=abs(difference),
        number={
            "prefix": f"<span style='color:{change_color};font-size:0.5em'>{change_direction} $</span>",
            "valueformat": ",",
            "font": {"size": 32, "family": "Arial", "color": change_color},
        },
        title={
            "text": f"<b>{title}</b>",
            "font": {"size": 14, "family": "Arial", "color": KENYA_THEME["dark"]},
        },
        domain={'x': [0.3, 0.7], 'y': [0.6, 0.9]},
    ))
    
    # Current period total (top left)
    fig.add_trace(go.Indicator(
        mode="number",
        value=current_total,
        number={
            "prefix": "<span style='font-size:0.5em'>$</span>",
            "valueformat": ",",
            "font": {"size": 20, "family": "Arial", "color": KENYA_THEME["dark"]},
        },
        title={
            "text": current_label,
            "font": {"size": 12, "family": "Arial", "color": KENYA_THEME["dark"]},
        },
        domain={'x': [0.1, 0.45], 'y': [0.2, 0.4]},
    ))
    
    # Previous period total (top right)
    fig.add_trace(go.Indicator(
        mode="number",
        value=previous_total,
        number={
            "prefix": "<span style='font-size:0.5em'>$</span>",
            "valueformat": ",",
            "font": {"size": 20, "family": "Arial", "color": KENYA_THEME["dark"]},
        },
        title={
            "text": previous_label,
            "font": {"size": 12, "family": "Arial", "color": KENYA_THEME["dark"]},
        },
        domain={'x': [0.55, 0.9], 'y': [0.2, 0.4]},
    ))
    
    # Percentage change (bottom center)
    fig.add_trace(go.Indicator(
        mode="number",
        value=abs(pct_change),
        number={
            "suffix": "%",
            "valueformat": ".1f",
            "font": {"size": 20, "family": "Arial", "color": change_color},
        },
        title={
            "text": "PERCENTAGE CHANGE",
            "font": {"size": 12, "family": "Arial", "color": KENYA_THEME["dark"]},
        },
        domain={'x': [0.3, 0.7], 'y': [0.1, 0.2]},
    ))
    
    fig.update_layout(
        plot_bgcolor=KENYA_THEME["light"],
        paper_bgcolor=KENYA_THEME["light"],
        margin=dict(l=10, r=10, t=50, b=10),
        height=180,  # Slightly taller to accommodate extra info
        font={"family": "Arial"}
    )
    
    return fig

def create_top_changes_chart(current_month="Feb_23"):
    month_columns = [col for col in df.columns if col != 'Region/Country']
    current_index = month_columns.index(current_month)
    previous_month = month_columns[current_index - 1] if current_index > 0 else None
    
    if not previous_month:
        return go.Figure()
    
    df['Difference'] = df[current_month] - df[previous_month]
    df_sorted = df[['Region/Country', 'Difference']].copy()
    top_increase = df_sorted.sort_values(by='Difference', ascending=False).head(5)
    top_decrease = df_sorted.sort_values(by='Difference', ascending=True).head(5)
    combined = pd.concat([top_increase, top_decrease]).sort_values(by='Difference')
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=combined['Region/Country'],
        x=combined['Difference'],
        orientation='h',
        marker_color=combined['Difference'].apply(lambda x: KENYA_THEME["primary"] if x >= 0 else KENYA_THEME["secondary"]),
        text=combined['Difference'].apply(lambda x: f"${x:,.0f}"),
        textposition='auto',
        hovertemplate='%{y}: %{text}<extra></extra>',
    ))
    
    fig.update_layout(
        title=f"Top Changes ({previous_month.replace('_', ' ')} → {current_month.replace('_', ' ')})",
        xaxis_title="Change in Remittance (USD)",
        yaxis_title="Region/Country",
        plot_bgcolor=KENYA_THEME["light"],
        paper_bgcolor=KENYA_THEME["light"],
        height=400,
        margin=dict(l=40, r=40, t=80, b=40),
        font=dict(size=12),
    )
    
    return fig

def create_trend_chart(current_month="Feb_23"):
    non_month_cols = ["Region/Country"]
    month_cols = [col for col in df.columns if col not in non_month_cols]
    
    current_index = month_cols.index(current_month)
    if current_index < 11:
        return go.Figure()
    
    last_12_months = month_cols[current_index - 11 : current_index + 1]
    df["Total_12_Months"] = df[last_12_months].sum(axis=1)
    top_5 = df.sort_values("Total_12_Months", ascending=False).head(5)
    
    fig = go.Figure()
    
    # Add U.S.A. line if exists
    usa_rows = df[df["Region/Country"] == "U.S.A"]
    if not usa_rows.empty:
        usa_data = usa_rows.iloc[0]
        fig.add_trace(go.Scatter(
            x=last_12_months,
            y=usa_data[last_12_months],
            mode="lines+markers",
            name="U.S.A",
            line=dict(dash="dash", color=KENYA_THEME["dark"], width=3),
            marker=dict(symbol="circle", size=6)
        ))
    
    # Add top 5 countries (skip U.S.A if already plotted)
    for _, row in top_5.iterrows():
        country = row["Region/Country"]
        if country == "U.S.A":
            continue
        fig.add_trace(go.Scatter(
            x=last_12_months,
            y=row[last_12_months],
            mode="lines+markers",
            name=country
        ))
    
    fig.update_layout(
        title=f"12-Month Trend (Ending {current_month.replace('_', ' ')})",
        xaxis_title="Month",
        yaxis_title="Remittance Amount (Log Scale)",
        legend_title="Region/Country",
        height=400,
        plot_bgcolor=KENYA_THEME["light"],
        paper_bgcolor=KENYA_THEME["light"],
        margin=dict(l=40, r=40, t=80, b=40)
    )
    fig.update_yaxes(type="log")
    
    return fig

def create_choropleth_map(current_month="Jan_23"):
    filtered_data = df_melted[df_melted['Month_Year'] == current_month] if current_month in df_melted['Month_Year'].values else df_melted
    
    choropleth_fig = px.choropleth(
        filtered_data,
        locations="Region/Country",
        locationmode="country names",
        color="Value",
        hover_data=["Value"],
        title=f"Remittance Sources ({current_month.replace('_', ' ')})",
        color_continuous_scale="Viridis",
        range_color=(0, filtered_data["Value"].quantile(0.95)),
        height=400
    )
    choropleth_fig.update_layout(
        paper_bgcolor=KENYA_THEME["light"],
        plot_bgcolor=KENYA_THEME["light"]
    )
    
    return choropleth_fig

def create_bar_chart(current_month="Jan_23"):
    filtered_data = df_melted[df_melted['Month_Year'] == current_month] if current_month in df_melted['Month_Year'].values else df_melted
    bar_data = filtered_data.groupby("Region/Country")['Value'].sum().sort_values(ascending=False).head(10)
    
    bar_fig = px.bar(
        x=bar_data.values,
        y=bar_data.index,
        orientation='h',
        color=bar_data.values,
        color_continuous_scale=[KENYA_THEME["secondary"], KENYA_THEME["primary"]],
        title=f"Top 10 Countries by Remittance ({current_month.replace('_', ' ')})",
        labels={"x": "Remittance (USD)", "y": "Country"},
        height=400
    )
    bar_fig.update_layout(
        plot_bgcolor=KENYA_THEME["light"],
        paper_bgcolor=KENYA_THEME["light"]
    )
    
    return bar_fig

def create_sunburst_charts(current_month="Jan_23"):
    current_year = int(current_month.split('_')[1]) + 2000
    filtered_data = df_melted[df_melted['Month_Year'] == current_month] if current_month in df_melted['Month_Year'].values else df_melted
    year_data = df_melted[df_melted['Year'] == current_year]
    
    # 1. Country Breakdown for Selected Month
    sunburst_fig1 = px.sunburst(
        filtered_data,
        path=["Region/Country", "Month_Year"],
        values="Value",
        title=f"<b>Country Breakdown for {current_month.replace('_', ' ')}</b>",
        labels={"Value": "Remittance (USD)"},
        color="Value",
        color_continuous_scale='RdBu',
        width=800,
        height=800
    )
    sunburst_fig1.update_traces(
        textinfo="label+value+percent entry",
        insidetextorientation='radial',
        textfont=dict(size=18, family="Arial", color="black"),  # Larger text
        marker=dict(line=dict(color='white', width=1.5)),  # Thicker borders
        hovertemplate='<b>%{label}</b><br>Amount: $%{value:,}<br>%{percentEntry:.1%} of total<extra></extra>'
    )
    
    # 2. Yearly Accumulation by Month
    sunburst_fig2 = px.sunburst(
        year_data.sort_values(by="Month_Year"),
        path=["Year", "Month_Year", "Region/Country"],
        values="Value",
        title=f"<b>Yearly Accumulation ({current_year})</b>",
        labels={"Value": "Remittance (USD)"},
        color="Value",
        color_continuous_scale='RdBu',
        width=800,
        height=800
    )
    sunburst_fig2.update_traces(
        textinfo="label+value+percent entry",
        insidetextorientation='radial',
        textfont=dict(size=18, family="Arial", color="black"),  # Larger text
        marker=dict(line=dict(color='white', width=1.5)),  # Thicker borders
        hovertemplate='<b>%{label}</b><br>Amount: $%{value:,}<br>%{percentEntry:.1%} of total<extra></extra>'
    )
    
    # Standard layout for both charts
    for fig in [sunburst_fig1, sunburst_fig2]:
        fig.update_layout(
            uniformtext=dict(minsize=16, mode='hide'),  # Prevent text hiding
            title_font=dict(size=20, family="Arial"),  # Larger titles
            coloraxis_colorbar=dict(
                title='USD Amount',
                thickness=20,
                len=0.6
            ),
            margin=dict(l=50, r=50, t=100, b=50)  # Adequate spacing
        )
    
    return sunburst_fig1, sunburst_fig2

# App layout (same as before)
app.layout = dbc.Container(
    fluid=True,
    style={"padding": "2rem", "backgroundColor": "#01030E"},
    children=[
        # Header Section
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H1(
                            "KENYA REMITTANCE DASHBOARD",
                            className="text-center mb-2",
                            style={"fontWeight": "bold", "letterSpacing": "1px"}
                        ),
                        html.P(
                            "Tracking diaspora remittances to Kenya ('000 USD)",
                            className="text-center",
                            style={"fontSize": "1.1rem"}
                        )
                    ],
                    style=CUSTOM_STYLES["header"]
                ),
                width=12
            )
        ),
        
        # Control Row
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label(
                            "SELECT MONTH/YEAR:",
                            className="font-weight-bold",
                            style={"color": KENYA_THEME["dark"]}
                        ),
                        dcc.Dropdown(
                            id="month-dropdown",
                            options=[
                                {"label": col.replace("_", " ").upper(), "value": col} 
                                for col in dt.columns if col != "Region/Country"
                            ],
                            value="Jan_23",
                            clearable=False,
                            style=CUSTOM_STYLES["dropdown"]
                        )
                    ],
                    md=4
                ),
                dbc.Col(
                    html.Div(
                        "Latest Data: " + dt.columns[-1].replace("_", " ").upper(),
                        className="text-right pt-3",
                        style={
                            "color": KENYA_THEME["secondary"],
                            "fontWeight": "bold",
                            "fontSize": "1.1rem"
                        }
                    ),
                    md=8,
                    className="d-flex align-items-center justify-content-end"
                )
            ],
            className="mb-4"
        ),
        
        # KPI Cards Row
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.Img(src="/assets/icons/m.png", style={
                                            "height": "100px",
                                            "position": "absolute",
                                            "top": "10px",
                                            "left": "10px",
                                            "zIndex": "1"
                                }),
                            dcc.Graph(id="total-indicator", config={"displayModeBar": False})
            ]),
                        style=CUSTOM_STYLES["card"]
                    ),
                    md=4
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                             html.Img(src="/assets/icons/month.webp", style={
                                            "height": "100px",
                                            "position": "absolute",
                                            "top": "10px",
                                            "left": "10px",
                                            "zIndex": "1"
                                }),
                            dcc.Graph(id="change-indicator", config={"displayModeBar": False})
            ]),
                        style=CUSTOM_STYLES["card"]
                    ),
                    md=4
                ),
                
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.Img(src="/assets/icons/xl.png", style={
                                            "height": "100px",
                                            "position": "absolute",
                                            "top": "10px",
                                            "left": "10px",
                                            "zIndex": "1"
                                }),
                            dcc.Graph(id="yoy-change-indicator", config={"displayModeBar": False})
            ]),
                        style=CUSTOM_STYLES["card"]
                    ),
                    md=4
                )
            ],
            className="mb-4"
        ),
        
        # Main Charts Row 1
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Img(
                                    src=r"C:\Users\KMC\Desktop\ds\remitances\Kenya-remittance-dashboard\src\icons\budget.png", 
                                    style={
                                        "height": "200px", 
                                        "marginRight": "100px",
                                        "verticalAlign": "middle"
                                    }),
                                html.H5(
                                    "TOP CHANGES",
                                    className="card-title",
                                    style={"color": KENYA_THEME["primary"]}
                                ),
                                dcc.Graph(id="top-changes-chart")
                            ]
                        ),
                        
                        style=CUSTOM_STYLES["card"]
                    ),
                    md=6
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "12-MONTH TREND",
                                    className="card-title",
                                    style={"color": KENYA_THEME["primary"]}
                                ),
                                dcc.Graph(id="trend-chart")
                            ]
                        ),
                        style=CUSTOM_STYLES["card"]
                    ),
                    md=6
                )
            ],
            className="mb-4"
        ),
        
        # Main Charts Row 2
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "GEOGRAPHIC DISTRIBUTION",
                                    className="card-title",
                                    style={"color": KENYA_THEME["primary"]}
                                ),
                                dcc.Graph(id="choropleth-map")
                            ]
                        ),
                        style=CUSTOM_STYLES["card"]
                    ),
                    md=6
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "TOP COUNTRIES",
                                    className="card-title",
                                    style={"color": KENYA_THEME["primary"]}
                                ),
                                dcc.Graph(id="bar-chart")
                            ]
                        ),
                        style=CUSTOM_STYLES["card"]
                    ),
                    md=6
                )
            ],
            className="mb-4"
        ),  
        # Trend Analysis Row
        # sunbrust chart:
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "REMITTANCE BY COUNTRY",
                                    className="card-title",
                                    style={"color": KENYA_THEME["primary"]}
                                ),
                                dcc.Graph(id="sunburst-country")
                            ]
                        ),
                        style=CUSTOM_STYLES["card"]
                    ),
                    md=6
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "REMITTANCE BY MONTH",
                                    className="card-title",
                                    style={"color": KENYA_THEME["primary"]}
                                ),
                                dcc.Graph(id="sunburst-month")
                            ]
                        ),
                        style=CUSTOM_STYLES["card"]
                    ),
                    md=6
                )
            ],
            className="mb-4"
        ),
        
        # Footer
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("DATA SOURCES & METHODOLOGY", className="card-title"),
                            html.P(
                                "This dashboard tracks remittance flows to Kenya from diaspora communities worldwide. "
                                "All amounts are shown in thousands of USD equivalent.",
                                className="card-text"
                            ),
                            html.P([
                                "Data Source: ",
                                html.A(
                                    "Central Bank of Kenya",
                                    href="https://www.centralbank.go.ke/diaspora-remittances/",
                                    target="_blank",
                                    style={"color": KENYA_THEME["primary"]}
                                )
                            ]),
                            html.P("Missing data handling methodology:"),
                            html.Ul([
                                html.Li("Bahamas (April 2020): Used NOCB (Next Observation Carried Backward)"),
                                html.Li("Iraq (May 2021): Applied LOCF (Last Observation Carried Forward)"),
                                html.Li("Iraq (June 2021): Used NOCB"),
                                html.Li("China (April 2021): Replaced with mean from six-month window")
                            ]),
                            html.Hr(),
                            html.Footer(
                                [
                                    html.P(
                                        "Developed by Samy Migwi | Data Scientist",
                                        className="mb-1"
                                    ),
                                    html.P(
                                        "© 2025 All Rights Reserved",
                                        className="text-muted small"
                                    )
                                ],
                                style={
                                    "textAlign": "center",
                                    "color": KENYA_THEME["dark"]
                                }
                            )
                        ]
                    ),
                    style={
                        "backgroundColor": KENYA_THEME["light"],
                        "border": "none"
                    }
                ),
                width=12
            )
        )
    ]
)

# Callback implementation
@app.callback(
    [Output("total-indicator", "figure"),
     Output("change-indicator", "figure"),
     Output("yoy-change-indicator", "figure"),
     Output("top-changes-chart", "figure"),
     Output("trend-chart", "figure"),
     Output("choropleth-map", "figure"),
     Output("bar-chart", "figure"),
     Output("sunburst-country", "figure"),  # New output
     Output("sunburst-month", "figure")],   # New output
    [Input("month-dropdown", "value")]
)
def update_dashboard(selected_month):
    total_fig = create_total_indicator(selected_month)
    change_fig = create_change_indicator(selected_month, "month")
    yoy_change_fig = create_change_indicator(selected_month, "year")
    changes_chart = create_top_changes_chart(selected_month)
    trend_chart = create_trend_chart(selected_month)
    choropleth_fig = create_choropleth_map(selected_month)
    bar_fig = create_bar_chart(selected_month)
    sunburst_country, sunburst_month = create_sunburst_charts(selected_month)  # Unpack both figures
    
    return (
        total_fig, 
        change_fig, 
        yoy_change_fig,
        changes_chart, 
        trend_chart, 
        choropleth_fig, 
        bar_fig,
        sunburst_country,  # Country-focused sunburst
        sunburst_month    # Month-focused sunburst
    )
    
import os
print("Current working directory:", os.getcwd())

if __name__ == "__main__":
    app.run(debug=True)