from dataclasses import dataclass, field
from typing import List


@dataclass
class Coordinate:
    x: int
    y: int


@dataclass
class Polygon:
    id: str
    type: str
    coordinates: List[Coordinate] = field(default_factory=list)
