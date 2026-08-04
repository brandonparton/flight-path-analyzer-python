from pandas import DataFrame
import plotly.graph_objects as go


def create_flight_path(df: DataFrame) -> None:
    """
    Create a 3D visualization of the aircraft flight path.

    The path is plotted using:
    - Longitude as X axis
    - Latitude as Y axis
    - Altitude as Z axis

    Altitude is represented through line and marker color.
    """

    fig = go.Figure()

    # Flight path line
    fig.add_trace(
    go.Scatter3d(
        x=df["longitude"],
        y=df["latitude"],
        z=df["altitude"],
        mode="lines+markers",
        line=dict(
            color=df["altitude"],
            colorscale="Viridis",
            width=6,
        ),
        marker=dict(
            size=3,
            color=df["altitude"],
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(
                title="Altitude (ft)",
                len=0.6,
                thickness=15,
            )
        ),
        name="Flight Path",
    )
)

    # Starting point
    fig.add_trace(
        go.Scatter3d(
            x=[df["longitude"].iloc[0]],
            y=[df["latitude"].iloc[0]],
            z=[df["altitude"].iloc[0]],
            mode="markers",
            marker=dict(
                size=8,
                color="#00ff00"
            ),
            name="Takeoff",
        )
    )

    # Ending point
    fig.add_trace(
        go.Scatter3d(
            x=[df["longitude"].iloc[-1]],
            y=[df["latitude"].iloc[-1]],
            z=[df["altitude"].iloc[-1]],
            mode="markers",
            marker=dict(
                size=8,
                color="#ff3333"
            ),
            name="Landing",
        )
    )

    fig.update_layout(
        title="3D Flight Path Visualization",
        paper_bgcolor="black",
        font=dict(
            color="white",
            size=12,
        ),
        scene=dict(
            xaxis=dict(
                title="Longitude",
                backgroundcolor="#111",
                gridcolor="#333",
            ),
            yaxis=dict(
                title="Latitude",
                backgroundcolor="#111",
                gridcolor="#333",
            ),
            zaxis=dict(
                title="Altitude (ft)",
                backgroundcolor="#111",
                gridcolor="#333",
            ),
            aspectmode="manual",
            aspectratio=dict(
                x=1.2,
                y=1,
                z=0.6,
            ),
            camera=dict(
                eye=dict(
                    x=1.8,
                    y=1.2,
                    z=0.9,
                )
            ),
        ),
        margin=dict(
            t=80,
            b=30,
            l=0,
            r=0,
        ),
        legend=dict(
            x=0,
            y=1,
            bgcolor="rgba(0,0,0,0.5)",
        )
    )

    fig.show()