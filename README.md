# Steam-Search *Rofi edition*

![Steam Search using icon type](/screenshots/screenshot3.png)

## Installation

### Manual Install

1. Download the `steam-search.pyz` from here: [Releases](https://github.com/Garulf/Steam-Search-rofi/releases)
2. Move `steam-search.pyz` to your Rofi scripts directory (~/.config/rofi/scripts)
3. Run `chmod +x ./steam-search.pyz` to allow Steam Search to run.

## Usage

Steam Search can be launched easily with:
```
rofi -modes steam-search -show steam-search
```

## Options

Steam Search allows you to customize some of its features using environmental variables.

| ENV        | DEFAULT              | INPUT                   | Description                                                     |
|------------|----------------------|-------------------------|-----------------------------------------------------------------|
| STEAM_PATH | ~/.local/share/steam | Steam install directory | This is the path Steam Search uses to find your Steam library.  |
| ICON_TYPE  | icon                 | icon, grid              | Set what type of image Steam Search will use for icons in Rofi. |

example:
```
ICON_TYPE=grid rofi -modes steam-search -show steam-search
```

## More screenshots

![Steam Search using grid icon type](/screenshots/screenshot2.png)
