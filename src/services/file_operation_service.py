"""
Service for file operations (Copy and Remove).
"""
import shutil
from pathlib import Path


class FileOperationService:
    """
    Handles safe file copying and removal for the Photo Picker workflow.
    Never modifies original files.
    """

    @staticmethod
    def copy_file(source_path: str, destination_folder: str) -> bool:
        """
        Copies the source file to the destination folder.
        Returns True if successful or if file already exists.
        Returns False on failure.
        """
        src = Path(source_path)
        dst_dir = Path(destination_folder)
        
        if not src.exists() or not src.is_file():
            print(f"FileOperationService: Source file not found: {source_path}")
            return False
            
        if not dst_dir.exists():
            dst_dir.mkdir(parents=True, exist_ok=True)
            
        dst = dst_dir / src.name
        
        if dst.exists():
            # Idempotent: If it's already there, consider it a success
            return True
            
        try:
            shutil.copy2(src, dst)
            return True
        except Exception as e:
            print(f"FileOperationService: Failed to copy {source_path} to {dst}: {e}")
            return False

    @staticmethod
    def remove_file(source_path: str, destination_folder: str) -> bool:
        """
        Removes the copied file from the destination folder (Undo action).
        Does NOT touch the original source_path.
        Returns True if successfully removed or if it didn't exist.
        """
        src = Path(source_path)
        dst_dir = Path(destination_folder)
        
        dst = dst_dir / src.name
        
        if not dst.exists():
            return True
            
        try:
            dst.unlink()
            return True
        except Exception as e:
            print(f"FileOperationService: Failed to remove {dst}: {e}")
            return False
