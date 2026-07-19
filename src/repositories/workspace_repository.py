"""
Repository for managing Workspace storage.
"""
import json
import re
from pathlib import Path
from typing import Optional, List

from src.domain.workspace import Workspace
from src.config.constants import WORKSPACES_DIR


class WorkspaceRepository:
    """
    Handles reading and writing Workspace data to the file system.
    """

    def __init__(self, base_dir: Path = WORKSPACES_DIR) -> None:
        self.base_dir = base_dir
        # Ensure base workspace directory exists
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _sanitize_name(self, name: str) -> str:
        """Convert workspace name to a safe folder name."""
        # Lowercase, replace non-alphanumeric with hyphen, remove consecutive hyphens
        safe = re.sub(r"[^\w]+", "-", name.lower()).strip("-")
        return safe or "default"

    def _get_workspace_path(self, name: str) -> Path:
        """Get the absolute path to a workspace folder."""
        safe_name = self._sanitize_name(name)
        return self.base_dir / safe_name

    def save(self, workspace: Workspace) -> None:
        """
        Save a workspace and its selections to the file system.
        """
        workspace_dir = self._get_workspace_path(workspace.name)
        workspace_dir.mkdir(parents=True, exist_ok=True)

        workspace.mark_updated()

        # Save metadata (workspace.json)
        workspace_file = workspace_dir / "workspace.json"
        metadata = {
            "name": workspace.name,
            "source_folder": workspace.source_folder,
            "destination_folder": workspace.destination_folder,
            "current_index": workspace.current_index,
            "total_images": workspace.total_images,
            "created_at": workspace.created_at,
            "updated_at": workspace.updated_at
        }
        with open(workspace_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Save selections (selections.json)
        selections_file = workspace_dir / "selections.json"
        with open(selections_file, "w", encoding="utf-8") as f:
            json.dump(workspace.selected_images, f, indent=2, ensure_ascii=False)

    def load(self, name: str) -> Optional[Workspace]:
        """
        Load a workspace by name. Returns None if not found.
        """
        workspace_dir = self._get_workspace_path(name)
        workspace_file = workspace_dir / "workspace.json"
        selections_file = workspace_dir / "selections.json"

        if not workspace_file.exists():
            return None

        try:
            with open(workspace_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            
            selected_images: List[str] = []
            if selections_file.exists():
                with open(selections_file, "r", encoding="utf-8") as f:
                    selected_images = json.load(f)

            return Workspace(
                name=metadata.get("name", name),
                source_folder=metadata.get("source_folder", ""),
                destination_folder=metadata.get("destination_folder", ""),
                current_index=metadata.get("current_index", 0),
                total_images=metadata.get("total_images", 0),
                created_at=metadata.get("created_at", ""),
                updated_at=metadata.get("updated_at", ""),
                selected_images=selected_images
            )
        except Exception:
            return None
