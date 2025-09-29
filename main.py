import subprocess
import importlib.util
import os

# Get compute.py from a previous commit
commit_id = "ee6bab9381acadaed7b0b8632071977b4aa15f62"  
result = subprocess.run(f"git show {commit_id}:compute.py", shell=True, capture_output=True, text=True, check=True)

# Write to temporary file
with open("compute_old.py", 'w') as f:
    f.write(result.stdout)

# Import the old version
spec = importlib.util.spec_from_file_location("compute_old", "compute_old.py")
compute_old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compute_old)

# Use the old add function
print(compute_old.add(3))

# Clean up
os.remove("compute_old.py")