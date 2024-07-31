from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from typing import TYPE_CHECKING

import vdf  # type: ignore

if TYPE_CHECKING:
    from steam_client.steam import Steam

from .shortcut import Shortcut

STEAM64_OFFSET = 76561197960265728


@dataclass
class User:
    id: int
    data: UserData


@dataclass
class UserData:
    AccountName: str
    PersonaName: str
    RememberPassword: str
    WantsOfflineMode: str
    SkipOfflineModeWarning: str
    AllowAutoLogin: str
    MostRecent: str
    Timestamp: str


class LoginUser:
    """Represents a current or previous logged in Steam user."""

    def __init__(self, steam: Steam, user: User):
        self._steam = steam
        self.user = user

    @property
    def is_most_recent(self) -> bool:
        """Returns whether the user is the most recent user."""
        return self.user.data.MostRecent == '1'

    @property
    def steam_id3(self) -> int:
        """Returns the last portion of the user's SteamID3."""
        steamidacct = (int(self.user.id) - STEAM64_OFFSET)
        return steamidacct

    @property
    def user_data_dir(self) -> Path:
        """Returns the path to the userdata folder."""
        return Path(self._steam.base_path).joinpath('userdata', str(self.steam_id3))

    @property
    def config(self) -> Path:
        """Returns the path to the config folder."""
        return Path(self.user_data_dir).joinpath('config')

    @property
    def shortcuts_file(self) -> Path:
        """Returns the path to the shortcuts.vdf file."""
        return Path(self.config).joinpath('shortcuts.vdf')

    @property
    def grid_path(self) -> Path:
        """Returns the path to the user's shortcut grid images."""
        return Path(self.user_data_dir).joinpath('config', 'grid')

    def shortcuts(self) -> List[Shortcut]:
        """Returns the data from the shortcuts.vdf file."""
        with open(self.shortcuts_file, 'rb') as f:
            shortcuts = vdf.binary_load(f)
        return [Shortcut(self._steam, self, shortcuts['shortcuts'][shortcut_idx]) for shortcut_idx in shortcuts['shortcuts']]


class LoginUsers:
    """Represents the loginusers.vdf file."""

    def __init__(self, steam: Steam):
        self._steam = steam

    @property
    def _path(self) -> Path:
        """Returns the path to the loginusers.vdf file."""
        return Path(self._steam.base_path).joinpath('config', 'loginusers.vdf')

    def users(self) -> List[LoginUser]:
        """Returns the users from the loginusers.vdf file."""
        with open(self._path, 'r', encoding='utf-8', errors='ignore') as f:
            login_users = vdf.load(f)
        return [LoginUser(self._steam, User(int(user_id), user_data)) for user_id, user_data in login_users['users'].items()]

    def most_recent_user(self) -> Optional[LoginUser]:
        """Returns the most recent user from the loginusers.vdf file."""
        return next((user for user in self.users() if user.is_most_recent), None)
