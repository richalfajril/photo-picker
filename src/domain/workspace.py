"""
Domain model for Workspace.
"""
from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class Workspace:
    """
    Represents the state of a Photo Picker session.
    Workspace is the aggregate root for the domain.
    """
    name: str
    source_folder: str
    destination_folder: str
    current_index: int = 0
    total_images: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # In-memory lists (selections are saved separately, image_list is loaded dynamically)
    selected_images: List[str] = field(default_factory=list)
    image_list: List[str] = field(default_factory=list)

    def mark_updated(self) -> None:
        """Update the last modified timestamp."""
        self.updated_at = datetime.now().isoformat()
