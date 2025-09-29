import git
import logging
import os
import tempfile
import importlib.util
import sys
import uuid
import threading

logger = logging.getLogger(__name__)

class GitFileManager:
    """Context manager for git file operations with automatic cleanup."""
    
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.checked_out_files = []
        self.loaded_modules = []
        self.repo = None
        self._lock = threading.RLock()
    
    def __enter__(self):
        with self._lock:
            try:
                self.repo = git.Repo(self.repo_path)
                logger.info(f"GitFileManager initialized for repo: {self.repo_path}")
                return self
            except Exception as e:
                logger.error(f"Failed to initialize GitFileManager: {e}")
                raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        with self._lock:
            self.cleanup()
            if exc_type:
                logger.error(f"GitFileManager exiting due to exception: {exc_val}")
    
    def checkout_file(self, commit_id, file_path, destination_path=None):
        """Checkout a specific file from a commit."""
        with self._lock:
            try:
                commit = self.repo.commit(commit_id)
                file_content = commit.tree[file_path].data_stream.read()
                
                if destination_path is None:
                    unique_id = f"{commit_id[:8]}_{uuid.uuid4().hex[:8]}_{len(self.checked_out_files)}"
                    filename = f"{os.path.basename(file_path)}_{unique_id}.py"
                    destination_path = os.path.join(tempfile.gettempdir(), filename)
                
                with open(destination_path, 'wb') as f:
                    f.write(file_content)
                
                self.checked_out_files.append(destination_path)
                logger.info(f"Checked out {file_path} from {commit_id[:8]} to {destination_path}")
                return destination_path
                
            except Exception as e:
                logger.error(f"Error checking out file: {e}")
                raise
    
    def checkout_and_load(self, commit_id, file_path, module_name):
        """Checkout a file and load it as a module."""
        with self._lock:
            try:
                temp_file = self.checkout_file(commit_id, file_path)
                unique_module_name = f"{module_name}_{commit_id[:8]}_{uuid.uuid4().hex[:8]}"
                
                spec = importlib.util.spec_from_file_location(unique_module_name, temp_file)
                module = importlib.util.module_from_spec(spec)
                sys.modules[unique_module_name] = module
                spec.loader.exec_module(module)
                
                self.loaded_modules.append(unique_module_name)
                logger.info(f"Loaded module {unique_module_name} from {temp_file}")
                return module
                
            except Exception as e:
                if 'unique_module_name' in locals() and unique_module_name in sys.modules:
                    del sys.modules[unique_module_name]
                logger.error(f"Error loading module: {e}")
                raise
    
    def cleanup(self):
        """Clean up all tracked files and modules."""
        with self._lock:
            for module_name in self.loaded_modules:
                try:
                    if module_name in sys.modules:
                        del sys.modules[module_name]
                except Exception as e:
                    logger.error(f"Failed to remove module {module_name}: {e}")
            
            for file_path in self.checked_out_files:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    logger.error(f"Failed to remove file {file_path}: {e}")
            
            self.checked_out_files.clear()
            self.loaded_modules.clear()
            logger.info("Cleanup completed")
    