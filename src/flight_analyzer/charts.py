from pandas import DataFrame
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# (column, display name, row, y-axis label, line color)
PLOTS = [
    ("altitude", "Altitude", 1, "Altitude (ft)", None),
    ("airspeed", "Airspeed", 2, "Airspeed (knots)", "orange"),
    ("pitch", "Pitch", 3, "Pitch / Roll (°)", "lightgreen"),
    ("roll", "Roll", 3, None, "red"),
    ("throttle", "Throttle", 4, "Throttle (%)", "yellow"),
    ("fuel", "Fuel", 5, "Fuel Remaining (%)", "skyblue"),
]


def create_charts(df: DataFrame) -> None:
    """
    Generate interactive telemetry charts.
    """

    fig = make_subplots(
        rows=5,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.07,
        row_heights=[1.5, 1.5, 1, 1, 1],
    )

    for column, name, row, ylabel, color in PLOTS:

        line = {}

        if color:
            line["color"] = color

        fig.add_trace(
            go.Scatter(
                x=df["time"],
                y=df[column],
                mode="lines",
                name=name,
                line=line,
            ),
            row=row,
            col=1,
        )

        if ylabel:
            fig.update_yaxes(
                title_text=ylabel,
                row=row,
                col=1,
            )

    fig.update_xaxes(
        title_text="Time (s)",
        row=5,
        col=1,
    )

    fig.update_layout(
        title="Flight Telemetry Overview",
        height=1200,
        paper_bgcolor="black",
        plot_bgcolor="#111111",
        font=dict(
            color="white",
            size=12,
        ),
        hovermode="x unified",
        margin=dict(
            t=80,
            b=60,
            l=70,
            r=30,
        ),
        legend=dict(
            orientation="h",
            x=0.5,
            y=-0.12,
            xanchor="center",
            yanchor="bottom",
        ),
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.show()