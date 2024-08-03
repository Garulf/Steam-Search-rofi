import winreg as reg
from winreg import HKEY_LOCAL_MACHINE

from .steam import Steam


STEAM_SUB_KEY = r'SOFTWARE\WOW6432Node\Valve\Steam'


def get_steam_from_registry() -> str:
    """Returns the Steam install path from the Windows registry."""
    with reg.OpenKey(HKEY_LOCAL_MACHINE, STEAM_SUB_KEY) as hkey:
        return reg.QueryValueEx(hkey, "InstallPath")[0]


def steam_from_registry() -> Steam:
    """Returns a Steam instance from the Windows registry."""
    return Steam(get_steam_from_registry())
