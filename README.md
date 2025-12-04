# DSC180A-Q1-Project
Repository for Quarter 1 Replication Project, DSC 180A  

## Overview 
This repository contains the implementation of our Q1 project, focused on point cloud matching, calculating distance mectrics, as well as optimal transport methods (W1, W2, Gromov-Wasserstein). This project explores how different profile matching and accuracy functions can be applied on MOCAP (motion-capture) data.


## Repository Structure
```
DSC180A-Q1-Project/
├─ datasets/                          # Folder for all data (raw and processed)
│  ├─ csv_files/                         # MoCap CSV files generated from TXT files (processed)
│  └─ txt_files/                         # Original MoCap TXT files (raw)
│
├─ src/                               # Root for all Python code
│  ├─ scripts/                          # CLI scripts to run tasks
│  │  ├─ __init__.py                     # Makes scripts/ a Python module
│  │  ├─ download_and_convert.py         # Script with main() to download and convert data
│  │  └─ run_pipeline.py                 # Script with main() to run the full pipeline
│  │
│  └─ dsc180a_q1_project/             # Main package
│     ├─ __init__.py                     # Exposes key utilities for easy imports
│     ├─ utils.py                        # Core classes/functions: LoadCloudPoint, DistanceProfile, plotting, accuracy
│     └─ datasets/                       # Helper modules for dataset handling
│        ├─ __init__.py                  # Makes datasets/ a Python module
│        ├─ download_mocap.py            # Functions to download MoCap data
│        └─ txt_to_csv.py                # Functions to convert TXT files to CSV   
├─ notebooks/                         # Used for visualizations
├─ scripts/
│   ├── matt_script.py                   # Multi-frame matching animation using OT plans
│   └── download_and_convert.py          # Downloads mocap data, converts CSV, runs GW
│
├─ setup.py                # Package setup file, defines dependencies and CLI entry points
├─ requirements.txt        # List of Python dependencies for pip
└─ README.md               # Project documentation
```

### Notebooks

All notebooks are in the `notebooks/` folder and are used for exploration, visualization, and testing of point cloud matching algorithms.

| Notebook | Purpose / Experiments |
|----------|---------------------|
| `distance_profile.ipynb` | Load and visualize point clouds, remove outliers, cluster joints, compute L2 distance profiles, 3D visualizations, and matching accuracy. |
| `distance_profile_qndo.ipynb` | Compare distance-profile OT (L1 & L2), vanilla OT, and GW OT matchings; visualize 3D matchings and compute accuracy. |
| `fused_gromov.ipynb` | Apply Fused Gromov-Wasserstein OT, sweep alpha parameters, evaluate multi-timestep accuracy, and compare with standard Wasserstein. |

## Running the Pipeline
 This project demonstrates point cloud matching on MOCAP data using Optimal Transport, Distance Profiling, and Gromov-Wasserstein methods.


### 1. Setup

Install the package and dependencies:

```bash
# Install locally in editable mode
pip install -e .
```

### 2. Data Acquisition

```bash 
# Download MoCap data (max 10,000 files)
download_csv

```

/// DOESNT WORK FROM THIS POINT FORWARD

### 3. Load Point Clouds
```bash 
from dsc180a_q1_project.utils import LoadCloudPoint

lcp = LoadCloudPoint(filepath="datasets/csv_files/0005_Jogging001.csv")
source_pc, target_pc = lcp.get_two_random_point_cloud()
```

### 4. Compute Distance Profiles
```bash
from dsc180a_q1_project.utils import DistanceProfile

dp = DistanceProfile(source_pc, target_pc)
distance_matrix = dp.compute_L2_matrix()
```

### 5. Run GW
```bash
import ot
from dsc180a_q1_project.utils import compute_W_matrix_distance_matrix_input, plot_3d_points_and_connections

W, map_matrix = compute_W_matrix_distance_matrix_input(distance_matrix[0], distance_matrix[1])
plot_3d_points_and_connections(source_pc, target_pc, map_matrix)

```


### SFU MOCAP data
run
```
    download_and_convert.py
```
This should download one of the mocap files and show the optimal transport matching between the first frame and the 500th frame. We've set the download and conversion limits as being 1, but feel free to remove those limits in script.py to download and convert the entire dataset.

![Image showing the matching between the first and 500th frame of mocap data](images/frame1_frame500_pairing_example.png)

## Sources/References
1. **Python Optimal Transport (POT)** – Library for optimal transport computations, including Wasserstein and Gromov-Wasserstein distances: [https://pythonot.github.io/](https://pythonot.github.io/)
2. **Motion Capture (MoCap) Dataset** – CMU MoCap database used for point cloud data: [https://mocap.cs.sfu.ca/](https://mocap.cs.sfu.ca/)
3. **Robust Point Matching with Distance Profiles** – Paper introducing distance-profile-based robust point cloud matching: [https://arxiv.org/pdf/2312.12641](https://arxiv.org/pdf/2312.12641)

