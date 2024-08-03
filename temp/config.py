import os
from pathlib import Path
from enum import Enum
from dataclasses import dataclass


DEFAULT_STEAM_PATH = Path.home() / ".local" / "share" / "Steam"

class IconType(str, Enum):
    GRID = "grid"
    ICON = "icon"


@dataclass
class Config:
    steam_path: str = DEFAULT_STEAM_PATH 
    icon_type: IconType = IconType.ICON

    def __post_init__(self):
        for opt in self.__dict__:
            env_name = opt.upper()
            if os.getenv(env_name):
                setattr(self, opt, os.getenv(env_name))

