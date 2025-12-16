# When checking if the graph connections are correct, check the 75th frame of datasets/csv_files/0005_Jogging001.csv. 
# This frame has no missing markers.

import pandas as pd
import numpy as np
import utils
import re
import plotly.graph_objects as go

def get_marker_name(col_name):
    """Extracts the marker name (e.g., 'M1') from a column name (e.g., 'M1_X')."""
    match = re.match(r"(M\d+)", col_name)
    if match:
        return match.group(1)
    return None

def create_skeleton_connections(df):
    """
    Creates a G matrix for plotting skeleton connections.
    This function assumes a specific mapping from M-markers to body parts.
    """
    
    # I think I need to put this inside a function that returns the csv or df,
    # but I'll leave it here for now.
    marker_mapping = {
        'M1': 'ARIEL',
        'M2': 'L_Head_Front',
        'M3': 'L_Head_Back',
        'M4': 'R_Head_Front',
        'M5': 'R_Head_Back',
        'M6': 'C7',
        'M7': 'T10',
        'M8': 'Clavicle',
        'M9': 'Sternum',
        'M10': 'L_Shoulder_Front',
        'M11': 'L_Shoulder_Back',
        'M12': 'L_Upper_Arm',
        'M13': 'L_Elbow',
        'M14': 'L_Elbow_Inner',
        'M15': 'L_Forearm',
        'M16': 'L_Wrist_Inner',
        'M17': 'L_Wrist_Outer',
        'M18': 'L_Hand_Inner',
        'M19': 'L_Hand_Outer',
        'M20': 'R_Shoulder_Front',
        'M21': 'R_Shoulder_Back',
        'M22': 'R_Upper_Arm',
        'M23': 'R_Elbow',
        'M24': 'R_Elbow_Inner',
        'M25': 'R_Forearm',
        'M26': 'R_Wrist_Inner',
        'M27': 'R_Wrist_Outer',
        'M28': 'R_Hand_Inner',
        'M29': 'R_Hand_Outer',
        'M30': 'L_Waist_Front',
        'M31': 'L_Waist_Mid',
        'M32': 'L_Waist_Back',
        'M33': 'R_Waist_Front',
        'M34': 'R_Waist_Mid',
        'M35': 'R_Waist_Back',
        'M36': 'L_Hip',
        'M37': 'L_Knee',
        'M38': 'L_Knee_Inner',
        'M39': 'L_Shin',
        'M40': 'L_Ankle',
        'M41': 'L_Heel',
        'M42': 'L_Metatarsal_5',
        'M43': 'L_Metatarsal_1',
        'M44': 'L_Toe',
        'M45': 'R_Hip',
        'M46': 'R_Knee',
        'M47': 'R_Knee_Inner',
        'M48': 'R_Shin',
        'M49': 'R_Ankle',
        'M50': 'R_Heel',
        'M51': 'R_Metatarsal_5',
        'M52': 'R_Metatarsal_1',
        'M53': 'R_Toe'
    }

    # Get the list of markers from the dataframe columns
    markers = []
    for col in df.columns:
        marker_name = get_marker_name(col)
        if marker_name and marker_name not in markers:
            markers.append(marker_name)
    
    num_markers = len(markers)
    G = np.zeros((num_markers, num_markers))

    # Define connections based on the assumed skeleton structure
    skeleton = [
        # Head
        ('L_Head_Front', 'ARIEL'), ('L_Head_Back', 'ARIEL'),
        ('R_Head_Front', 'ARIEL'), ('R_Head_Back', 'ARIEL'),
        ('L_Head_Front', 'L_Head_Back'), ('R_Head_Front', 'R_Head_Back'),
        ('L_Head_Front', 'R_Head_Front'),

        # Spine
        ('C7', 'ARIEL'), # Simplified connection to head
        ('C7', 'Sternum'), ('C7', 'Clavicle'), ('C7', 'T10'),

        # Torso
        ('Sternum', 'Clavicle'),
        ('T10', 'L_Waist_Back'), ('T10', 'R_Waist_Back'),
        ('L_Waist_Front', 'L_Waist_Mid'), ('L_Waist_Mid', 'L_Waist_Back'),
        ('R_Waist_Front', 'R_Waist_Mid'), ('R_Waist_Mid', 'R_Waist_Back'),
        ('L_Waist_Front', 'R_Waist_Front'), ('L_Waist_Back', 'R_Waist_Back'),
        ('Clavicle', 'R_Shoulder_Front'), ('Clavicle', 'L_Shoulder_Front'),

        # Right Arm
        ('R_Shoulder_Front', 'R_Shoulder_Back'),
        ('R_Shoulder_Front', 'R_Upper_Arm'),
        ('R_Upper_Arm', 'R_Elbow'),
        ('R_Elbow', 'R_Elbow_Inner'),
        ('R_Elbow', 'R_Forearm'),
        ('R_Forearm', 'R_Wrist_Inner'),
        ('R_Wrist_Inner', 'R_Wrist_Outer'),
        ('R_Wrist_Outer', 'R_Hand_Outer'),
        ('R_Hand_Outer', 'R_Hand_Inner'),
        
        # Left Arm
        ('L_Shoulder_Front', 'L_Shoulder_Back'),
        ('L_Shoulder_Front', 'L_Upper_Arm'),
        ('L_Upper_Arm', 'L_Elbow'),
        ('L_Elbow', 'L_Elbow_Inner'),
        ('L_Elbow', 'L_Forearm'),
        ('L_Forearm', 'L_Wrist_Inner'),
        ('L_Wrist_Inner', 'L_Wrist_Outer'),
        ('L_Wrist_Outer', 'L_Hand_Outer'),
        ('L_Hand_Outer', 'L_Hand_Inner'),
        
        # Hips
        ('L_Hip', 'L_Waist_Front'), ('R_Hip', 'R_Waist_Front'),
        ('L_Hip', 'L_Waist_Back'), ('R_Hip', 'R_Waist_Back'),
        ('L_Hip', 'R_Hip'),

        # Right Leg
        ('R_Hip', 'R_Knee'),
        ('R_Knee', 'R_Knee_Inner'),
        ('R_Knee', 'R_Shin'),
        ('R_Shin', 'R_Ankle'),
        ('R_Ankle', 'R_Heel'),
        ('R_Ankle', 'R_Metatarsal_1'),
        ('R_Ankle', 'R_Metatarsal_5'),
        ('R_Heel', 'R_Toe'),
        ('R_Metatarsal_1', 'R_Toe'),
        ('R_Metatarsal_5', 'R_Toe'),

        # Left Leg
        ('L_Hip', 'L_Knee'),
        ('L_Knee', 'L_Knee_Inner'),
        ('L_Knee', 'L_Shin'),
        ('L_Shin', 'L_Ankle'),
        ('L_Ankle', 'L_Heel'),
        ('L_Ankle', 'L_Metatarsal_1'),
        ('L_Ankle', 'L_Metatarsal_5'),
        ('L_Heel', 'L_Toe'),
        ('L_Metatarsal_1', 'L_Toe'),
        ('L_Metatarsal_5', 'L_Toe'),
    ]
    # Create a reverse mapping from body part name to M-label
    name_to_marker = {v: k for k, v in marker_mapping.items()}

    for p1, p2 in skeleton:
        if p1 in name_to_marker and p2 in name_to_marker:
            m1 = name_to_marker[p1]
            m2 = name_to_marker[p2]
            if m1 in markers and m2 in markers:
                idx1 = markers.index(m1)
                idx2 = markers.index(m2)
                G[idx1, idx2] = 1
                G[idx2, idx1] = 1
    
    return G, markers, marker_mapping

def animate_skeleton(df, G, num_frames=100):
    """
    Creates an animation of the skeleton over a number of frames.
    """
    points_list = []
    for i in range(num_frames):
        points = df.iloc[i].to_numpy().reshape(-1, 3)
        points_list.append(points)

    fig = go.Figure()

    # Initial frame
    points = points_list[0]
    fig.add_trace(go.Scatter3d(
        x=points[:, 2], y=points[:, 1], z=points[:, 0],
        mode='markers',
        marker=dict(size=5, color='blue'),
        name='Trackers'
    ))

    # Add lines for the initial frame
    for i in range(G.shape[0]):
        for j in range(i + 1, G.shape[1]):
            if G[i, j] != 0:
                p1 = points[i]
                p2 = points[j]
                fig.add_trace(go.Scatter3d(
                    x=[p1[2], p2[2]],
                    y=[p1[1], p2[1]],
                    z=[p1[0], p2[0]],
                    mode='lines',
                    line=dict(color="gray", width=2),
                    showlegend=False
                ))

    # Create frames for the animation
    frames = []
    for k in range(num_frames):
        points = points_list[k]
        frame_data = [go.Scatter3d(x=points[:, 2], y=points[:, 1], z=points[:, 0], mode='markers', marker=dict(size=5, color='blue'))]
        
        for i in range(G.shape[0]):
            for j in range(i + 1, G.shape[1]):
                if G[i, j] != 0:
                    p1 = points[i]
                    p2 = points[j]
                    frame_data.append(go.Scatter3d(
                        x=[p1[2], p2[2]],
                        y=[p1[1], p2[1]],
                        z=[p1[0], p2[0]],
                        mode='lines',
                        line=dict(color="gray", width=2),
                        showlegend=False
                    ))
        frames.append(go.Frame(data=frame_data, name=f'frame{k}'))

    fig.frames = frames

    # Animation layout
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='data'
        ),
        title_text='Skeleton Animation',
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}]),
                     dict(label='Pause',
                          method='animate',
                          args=[[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}])
            ])],
        sliders=[dict(
            steps=[dict(method='animate',
                        args=[[f'frame{k}'], {'frame': {'duration': 0, 'redraw': True}}],
                        label=str(k))
                   for k in range(num_frames)],
            active=0,
            currentvalue={"prefix": "Frame: "}
        )]
    )

    return fig


if __name__ == "__main__":
    # Load data
    lcp = utils.LoadCloudPoint(filepath="datasets/csv_files/0005_Jogging001.csv")
    df = lcp.load_df()

    # Create skeleton
    G, markers, marker_mapping = create_skeleton_connections(df)

    fig = animate_skeleton(df, G, num_frames=100)
    fig.show()
