from pathlib import Path
from typing import Union

from steam_client.steam import Steam
import rofi_menu

from config import Config

def get_games(steam_path: Union[str, Path]):
    steam = Steam(str(steam_path))
    return steam.library.games()

class MainMenu(rofi_menu.Menu):
    config = Config()
    prompt = "menu"
    items = []
    for _ in get_games(config.steam_path):
        items.append(
            rofi_menu.ShellItem(
                _.name,
                f"steam steam://rungameid/{_.appid}",
                icon=getattr(_, config.icon_type)
            )
        )

def run():
    rofi_menu.run(MainMenu(), rofi_version="1.6")  # change to 1.5 if you use older rofi version

if __name__ == "__main__":
    run()
