import os
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def load_data(filename):
    file_path = os.path.join("data", filename)
    with open(file_path, "r") as file:
        return json.load(file)


def create_charts(df):
    fig = make_subplots(
        rows=5,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.07,
        row_heights=[1.5, 1.5, 1, 1, 1],
    )

    fig.add_trace(
        go.Scatter(x=df["time"], y=df["altitude"], mode="lines", name="Altitude"),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=df["time"], y=df["airspeed"], mode="lines", name="Airspeed", line=dict(color="orange")),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(x=df["time"], y=df["pitch"], mode="lines", name="Pitch", line=dict(color="lightgreen")),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=df["time"], y=df["roll"], mode="lines", name="Roll", line=dict(color="red")),
        row=3, col=1
    )

    fig.add_trace(
        go.Scatter(x=df["time"], y=df["throttle"], mode="lines", name="Throttle", line=dict(color="yellow")),
        row=4, col=1
    )

    fig.add_trace(
        go.Scatter(x=df["time"], y=df["fuel"], mode="lines", name="Fuel", line=dict(color="skyblue")),
        row=5, col=1
    )

    fig.update_yaxes(title_text="Altitude (ft)", row=1, col=1)
    fig.update_yaxes(title_text="Airspeed (knots)", row=2, col=1)
    fig.update_yaxes(title_text="Pitch / Roll (°)", row=3, col=1)
    fig.update_yaxes(title_text="Throttle (%)", row=4, col=1)
    fig.update_yaxes(title_text="Fuel Remaining (%)", row=5, col=1)
    fig.update_xaxes(title_text="Time (s)", row=5, col=1)


    fig.update_layout(
        height=1200,
        title_text="Flight Telemetry Overview",
        paper_bgcolor="black",
        plot_bgcolor="#111",
        font=dict(color="white", size=12),
        hovermode="x unified",
        margin=dict(t=80, b=60, l=70, r=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.12,
            xanchor="center",
            x=0.5
        ),
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.show()


def create_flight_path(df):
    altitude_range = (df["altitude"] - df["altitude"].min()) / (df["altitude"].max() - df["altitude"].min())

    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=df["longitude"],
            y=df["latitude"],
            z=df["altitude"],
            mode="lines+markers",
            line=dict(
                color=df["altitude"],
                colorscale="Viridis",
                width=6
            ),
            marker=dict(
                size=4,
                color=df["altitude"],
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(
                    title=dict(
                        text="Altitude (ft)",
                        font=dict(color="white")
                    ),
                    tickfont=dict(color="white")
                )
            ),
            name="Flight Path",
        )
    )

    fig.update_layout(
        title="3D Flight Path Visualization",
        paper_bgcolor="black",
        font=dict(color="white", size=12),
        scene=dict(
            xaxis=dict(title="Longitude", backgroundcolor="#111", gridcolor="#333", showbackground=True, color="white"),
            yaxis=dict(title="Latitude", backgroundcolor="#111", gridcolor="#333", showbackground=True, color="white"),
            zaxis=dict(title="Altitude (ft)", backgroundcolor="#111", gridcolor="#333", showbackground=True, color="white"),
            aspectmode="manual",
            aspectratio=dict(x=1.2, y=1, z=0.6),
            camera=dict(
                eye=dict(x=1.8, y=1.2, z=0.9),
                center=dict(x=0, y=0, z=0)
            ),
        ),
        margin=dict(t=80, b=30, l=0, r=0),
    )

    fig.show()


def __main__():
    data = load_data("flight_data.json")
    df = pd.DataFrame(data)
    create_flight_path(df)
    create_charts(df)


if __name__ == "__main__":
    __main__()
