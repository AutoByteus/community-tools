from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class TransitStep:
    """Represents a single step in a transit journey"""
    mode: str  # e.g., "BUS", "TRAIN", "WALK"
    line: Optional[str] = None  # e.g., "S2", "350"
    line_color: Optional[str] = None  # e.g., "rgb(76, 144, 70)"
    duration_minutes: Optional[int] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    departure_stop: Optional[str] = None
    arrival_stop: Optional[str] = None

@dataclass
class Route:
    """Represents a complete transit route"""
    total_duration_minutes: int
    departure_time: datetime
    arrival_time: datetime
    steps: List[TransitStep]
    selected: bool = False  # Indicates if this is the currently selected route