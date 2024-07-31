from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING, Dict
from typing import TypedDict

import pycrc.algorithms as crc  # type: ignore

if TYPE_CHECKING:
    from .steam import Steam
    from .login_users import LoginUser

from .app import App


class ShortcutEntry(TypedDict):
    appid: int
    appname: str
    exe: str
    StartDir: str
    LaunchOptions: str
    icon: str
    tags: Dict[str, str]


class Shortcut(App):
    """Represents a Non-Steam Game shortcut."""

    def __init__(self, steam: Steam, user: LoginUser, data: ShortcutEntry):
        self._data = data
        self._user = user
        super().__init__(steam)

    def __repr__(self) -> str:
        return f'Shortcut(steam={self._steam.__repr__()}, data={self._data.__repr__()})'

    @property
    def name(self) -> str:
        return self._data["appname"]

    @property
    def appid(self) -> str:
        algorithm = crc.Crc(width=32, poly=0x04C11DB7, reflect_in=True,
                            xor_in=0xffffffff, reflect_out=True, xor_out=0xffffffff)
        input_string = ''.join([self._data["exe"], self._data["appname"]])
        top_32 = algorithm.bit_by_bit(input_string) | 0x80000000
        full_64 = (top_32 << 32) | 0x02000000
        return str(full_64)

    def _short_id(self) -> str:
        """
        Return Steam shortened App ID.
        This is primarily used for shortcuts in the grid.
        """
        return str(int(self.appid) >> int(32))

    @property
    def icon(self) -> Path:
        return Path(self._data["icon"]) or self._user.grid_path.joinpath(f"{self._short_id()}_icon.png")

    @property
    def header(self) -> Path:
        return self._user.grid_path.joinpath(f"{self._short_id()}.png")

    @property
    def grid(self) -> Path:
        return self._user.grid_path.joinpath(f"{self._short_id()}p.png")

    @property
    def hero(self) -> Path:
        return self._user.grid_path.joinpath(f"{self._short_id()}_hero.png")
