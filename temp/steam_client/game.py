from __future__ import annotations
import functools
from pathlib import Path
from typing import TYPE_CHECKING

import vdf

if TYPE_CHECKING:
    from .steam import Steam

from .app import App


UNKNOWN_GAME_NAME = 'UNKNOWN'


class SteamGame(App):
    """Represents a Steam game."""

    def __init__(self, steam: Steam, library_path: str, appid: str):
        self.library_path = library_path
        self._appid = appid
        super().__init__(steam)

    def __repr__(self) -> str:
        return f'Game(steam={self._steam.__repr__()}, library_path={self.library_path.__repr__()}, appid={self.appid.__repr__()})'

    @property
    def icon(self) -> Path:
        """Returns the path to the icon image."""
        return Path(self._steam.library_cache).joinpath(f'{self.appid}_icon.jpg')

    @property
    def header(self) -> Path:
        """Returns the path to the header image."""
        return Path(self._steam.library_cache).joinpath(f'{self.appid}_header.jpg')

    @property
    def grid(self) -> Path:
        """Returns the path to the 600x900 grid image."""
        return Path(self._steam.library_cache).joinpath(f'{self.appid}_library_600x900.jpg')

    @property
    def hero(self) -> Path:
        """Returns the path to the hero image."""
        return Path(self._steam.library_cache).joinpath(f'{self.appid}_library_hero.jpg')

    @property
    def hero_blur(self) -> Path:
        """Returns the path to the blurred hero image."""
        return Path(self._steam.library_cache).joinpath(f'{self.appid}_library_hero_blur.jpg')

    @property
    def manifest_path(self) -> Path:
        """Returns the path to the game's appmanifest."""
        return Path(self.library_path).joinpath('steamapps', f'appmanifest_{self.appid}.acf')

    @functools.cached_property
    def _manifest(self) -> dict:
        """Returns the data from the game's appmanifest."""
        try:
            with open(self.manifest_path, 'r', encoding='utf-8', errors='ignore') as f:
                manifest = vdf.load(f)
            return manifest
        except FileNotFoundError:
            return {}

    @functools.cached_property
    def name(self) -> str:
        """Returns the name of the game."""
        try:
            return self._manifest['AppState']['name']
        except KeyError:
            return UNKNOWN_GAME_NAME

    @property
    def appid(self) -> str:
        """Returns the app ID."""
        return self._appid

    def open_store_page(self):
        """Opens the game's store page in the Steam client."""
        self._steam.commands.store(self.appid)

    def uninstall(self):
        """Uninstalls the game."""
        self._steam.commands.uninstall(self.appid)
