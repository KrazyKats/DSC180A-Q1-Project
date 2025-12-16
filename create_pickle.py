
import numpy as np
import pickle
from utils import LoadCloudPoint, DistanceProfile

def create_pickle_file(csv_file_path, output_pickle_path):
    """
    Loads a point cloud from a CSV file, computes the distance matrix (adjacency matrix),
    and saves the point cloud (nodes) and the adjacency matrix to a pickle file.

    Args:
        csv_file_path (str): The path to the input CSV file.
        output_pickle_path (str): The path to the output pickle file.
    """
    lcp = LoadCloudPoint(filepath=csv_file_path)
    point_cloud = lcp.get_entire_point_cloud()

    nodes = point_cloud[74]

    # Compute the adjacency matrix (distance matrix)
    dist_profile = DistanceProfile(nodes, nodes)
    adjacency_matrix, _ = dist_profile.compute_L2_matrix()

    # The point cloud itself
    the_point_cloud = point_cloud

    # Create a dictionary to store the data
    data_to_pickle = {
        "nodes": nodes,
        "adjacency_matrix": adjacency_matrix,
        "point_cloud": the_point_cloud
    }

    with open(output_pickle_path, 'wb') as f:
        pickle.dump(data_to_pickle, f)

    print(f"Data from {csv_file_path} saved to {output_pickle_path}")

if __name__ == '__main__':
    csv_file = 'datasets/csv_files/0005_2FeetJump001.csv'
    pickle_file = 'data.pkl'

    create_pickle_file(csv_file, pickle_file)
