# Add project root (one level up) to Python path
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # go up 2 levels to repo root
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))
from dsc180a_q1_project import acc_dist_test, acc_full_test, acc_rem_test


def main():
    # Only averaging accuracy across two poses to save computation time, graphics in the paper were done with 100
    acc_full_test(num_poses = 2)
    acc_dist_test(num_poses = 2)
    acc_rem_test(num_poses = 2)


if __name__ == "__main__":
    main()
    