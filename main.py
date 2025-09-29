from git_utils import checkout_file_from_commit
import importlib.util
import sys

# Checkout the compute.py file from a previous commit
previous_commit_id = "ee6bab9381acadaed7b0b8632071977b4aa15f62"  # Replace with your actual commit ID
old_compute_file = checkout_file_from_commit(
    repo_path="/Users/avishsanthosh/Desktop/MuskCult",
    commit_id=previous_commit_id,
    file_path="compute.py",
    destination_path="compute_old.py"
)

# Import the old version dynamically
spec = importlib.util.spec_from_file_location("compute_old", old_compute_file)
compute_old = importlib.util.module_from_spec(spec)
sys.modules["compute_old"] = compute_old
spec.loader.exec_module(compute_old)

# Use the old version of the add function
print(compute_old.add(3))