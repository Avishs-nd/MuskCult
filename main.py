from git_utils import checkout_file_from_commit, load_module_from_commit

# Load the compute.py module from a previous commit directly into memory
previous_commit_id = "da84f9d20f8617e287413144d4f4b633bd64a16e"
compute_old = load_module_from_commit(
    repo_path="/Users/avishsanthosh/Desktop/MuskCult",
    commit_id=previous_commit_id,
    file_path="compute.py",
    module_name="compute_old"
)

# Use the old version of the add function
print(compute_old.add(3))