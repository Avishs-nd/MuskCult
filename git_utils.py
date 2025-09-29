import git
import os
import shutil
import tempfile
import logging

logger = logging.getLogger(__name__)

def checkout_file_from_commit(repo_path, commit_id, file_path, destination_path=None):
    """
    Checkout a specific file from a previous commit.
    
    Args:
        repo_path (str): Path to the git repository
        commit_id (str): The commit hash to checkout from
        file_path (str): Relative path to the file in the repo
        destination_path (str): Where to save the file (optional)
    
    Returns:
        str: Path to the checked out file
    """
    try:
        repo = git.Repo(repo_path)
        
        # Get the file content from the specific commit
        commit = repo.commit(commit_id)
        file_content = commit.tree[file_path].data_stream.read()
        
        # Determine destination
        if destination_path is None:
            destination_path = f"{file_path}_{commit_id[:8]}.py"
        
        # Write the file content
        with open(destination_path, 'wb') as f:
            f.write(file_content)
        
        logger.info(f"File {file_path} from commit {commit_id[:8]} saved to {destination_path}")
        return destination_path
        
    except Exception as e:
        logger.error(f"Error checking out file: {e}")
        raise