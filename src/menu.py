import os
from pathlib import Path

from steam_client.steam import Steam
import rofi_menu

DEFAULT_STEAM_PATH = Path.home() / ".local" / "share" / "Steam"

def get_games():
    steam_path = os.environ.get("STEAM_PATH", DEFAULT_STEAM_PATH)
    steam = Steam(str(steam_path))
    return steam.library.games()

class MainMenu(rofi_menu.Menu):
    prompt = "menu"
    items = []
    for _ in get_games():
        items.append(
            rofi_menu.ShellItem(_.name, f"steam steam://rungameid/{_.appid}", icon=_.icon)
        )

def run():
    rofi_menu.run(MainMenu(), rofi_version="1.6")  # change to 1.5 if you use older rofi version

if __name__ == "__main__":
    run()
