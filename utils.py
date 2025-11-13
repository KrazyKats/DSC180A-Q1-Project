import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import ot
import scipy as sp

def plot_3d_points_and_connections(points1, points2, G):
    # Ensure numpy arrays
    points1 = np.asarray(points1)
    points2 = np.asarray(points2)
    G = np.asarray(G)

    fig = go.Figure()

    # Plot first set of 3D points
    fig.add_trace(go.Scatter3d(
        x=points1[:, 0], y=points1[:, 1], z=points1[:, 2],
        mode='markers',
        marker=dict(size=5, color='blue'),
        name='Points 1'
    ))

    # Plot second set of 3D points
    fig.add_trace(go.Scatter3d(
        x=points2[:, 0], y=points2[:, 1], z=points2[:, 2],
        mode='markers',
        marker=dict(size=5, color='red'),
        name='Points 2'
    ))

    # Draw connections for nonzero G[i, j]
    for i in range(G.shape[0]):
        for j in range(G.shape[1]):
            if G[i, j] != 0:
                p1 = points1[i]
                p2 = points2[j]
                fig.add_trace(go.Scatter3d(
                    x=[p1[0], p2[0]],
                    y=[p1[1], p2[1]],
                    z=[p1[2], p2[2]],
                    mode='lines',
                    line=dict(color='gray', width=2),
                    showlegend=False
                ))

    # Layout styling
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='data'
        ),
        title='3D Points with Connections',
        template='plotly_white'
    )

    return fig

def compute_gw_and_plot(xs, xt):
    """
    Computes the GW plan between two points clouds and plots the results.
    """
    p = np.ones(xs.shape[0]) / xs.shape[0]
    q = np.ones(xt.shape[0]) / xt.shape[0]

    C1 = sp.spatial.distance.cdist(xs, xs)
    C2 = sp.spatial.distance.cdist(xt, xt)
    C1 /= C1.max()
    C2 /= C2.max()

    G0, log0 = ot.gromov.gromov_wasserstein(C1, C2, p, q, log = True, verbose = True)

    fig = plot_3d_points_and_connections(xt, xs, G0)
    print("hi")
    return fig, G0