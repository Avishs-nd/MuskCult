from git_utils import GitFileManager

commit_v2 = "d0f6317145dfaef548087ba2765c0c1df6b11122"
commit_v1 = "ee6bab9381acadaed7b0b8632071977b4aa15f62"

with GitFileManager("/Users/avishsanthosh/Desktop/MuskCult") as git_manager:
    compute_v1 = git_manager.checkout_and_load(commit_v2, "compute.py", "compute_v1")
    computed_value = compute_v1.add(5)
    print(computed_value)
        