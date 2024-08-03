from typing import Literal


SteamWindow = Literal[
    'main',
    'games',
    'games/details',
    'games/grid',
    'games/list',
    'friends',
    'chat',
    'bigpicture',
    'news',
    'settings',
    'tools',
    'console'
]


def run_game_id(app_id: str) -> str:
    """Launches game with the specified ID in the Steam client."""
    return f'steam://rungameid/{app_id}'


def store(app_id: str) -> str:
    """Opens the game's store page in the Steam client."""
    return f'steam://store/{app_id}'


def install(app_id: str) -> str:
    """Opens the game's install prompt in the Steam client."""
    return 'steam://install/{app_id}'


def uninstall(app_id: str) -> str:
    """Opens the game's uninstall prompt in the Steam client."""
    return f'steam://uninstall/{app_id}'


def update_news(app_id: str) -> str:
    """Opens the game's update news in the Steam client."""
    return f'steam://updatenews/{app_id}'


def open(window: SteamWindow) -> str:
    """Opens the specified window in the Steam client."""
    return f'steam://open/{window}'


def open_url(url: str) -> str:
    """Opens the specified URL in the Steam client."""
    return f'steam://openurl/{url}'
