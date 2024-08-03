from __future__ import annotations
from pathlib import Path
import hashlib
from typing import TYPE_CHECKING, List, Optional, Union

import vdf

from steam_client.shortcut import Shortcut

if TYPE_CHECKING:
    from .steam import Steam
from .library_directory import LibraryDirectory
from .game import SteamGame


class Library:
    """Represents the Steam library."""

    def __init__(self, steam: 'Steam'):
        self._steam = steam
        self._libraries_hash: Optional[str] = None
        self._libraries: List[LibraryDirectory] = []

    def _hash_steam_libraries(self) -> str:
        """Returns the MD5 hash of the Steam library folders file."""
        with open(str(self._steam.library_folders), 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def _is_updated(self) -> bool:
        """Returns whether the Steam library folders have been updated."""
        return self._libraries_hash != self._hash_steam_libraries()

    def _update_libraries(self):
        """Updates the Steam library folders."""
        with open(self._steam.library_folders, 'r', encoding='utf-8', errors='ignore') as f:
            libraries = vdf.load(f)
        # The is not always formatted the same way, so we grab the first key
        folder_key = list(libraries.keys())[0]
        self._libraries = [LibraryDirectory(self._steam, libraries[folder_key][item]["path"],
                                            libraries[folder_key][item]["apps"]) for item in libraries[folder_key]]

    def libraries(self) -> List[LibraryDirectory]:
        """Returns the Steam library folders."""
        if self._is_updated():
            self._libraries_hash = self._hash_steam_libraries()
            self._update_libraries()
        return self._libraries

    def games(self) -> List[SteamGame]:
        """Returns the games from the Steam library."""
        games = []
        for library in self.libraries():
            games.extend(library.get_games())
        return games

    def game_by_id(self, appid: str) -> Optional[SteamGame]:
        """Returns the game with the specified ID."""
        for game in self.games():
            if game.appid == appid:
                return game
        return None

    def game_by_name(self, name: str) -> Optional[SteamGame]:
        """Returns the game with the specified name."""
        for game in self.games():
            if game.name.casefold() == name.casefold():
                return game
        return None

    def shortcuts(self) -> List[Shortcut]:
        """Returns the Non-Steam shortcuts from the Steam library."""
        shortcuts = []
        for user in self._steam.login_users.users():
            shortcuts.extend(user.shortcuts())
        return shortcuts

    def all(self) -> List[Union[SteamGame, Shortcut]]:
        """Returns all the games and shortcuts from the Steam library."""
        return self.games() + self.shortcuts()
