from pathlib import Path
import webbrowser

from .library import Library
from .login_users import LoginUsers

DEFAULT_WIN_STEAM_PATH = r"c:\Program Files (x86)\Steam"


class Steam:
    """Represents the Steam client."""

    def __init__(self, base_path: str = DEFAULT_WIN_STEAM_PATH):
        self.base_path: str = base_path

    def __repr__(self) -> str:
        return f'Steam(base_path={self.base_path.__repr__()})'

    @property
    def app_cache(self) -> Path:
        """Returns the path to the appcache folder."""
        return Path(self.base_path).joinpath('appcache')

    @property
    def user_data(self) -> Path:
        """Returns the path to the userdata folder."""
        return Path(self.base_path).joinpath('userdata')

    @property
    def library_folders(self) -> Path:
        """Returns the path to the libraryfolders.vdf file."""
        return Path(self.base_path).joinpath('config', 'libraryfolders.vdf')

    @property
    def library_cache(self) -> Path:
        """Returns the path to the librarycache folder."""
        return Path(self.base_path).joinpath('appcache', 'librarycache')

    @property
    def users(self):
        return LoginUsers(self).users()

    @property
    def library(self) -> Library:
        return Library(self)

    def command(self, uri: str):
        return webbrowser.open(uri)
