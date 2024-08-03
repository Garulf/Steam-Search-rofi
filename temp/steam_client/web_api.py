from typing import Any, Dict

import requests  # type: ignore


BASE_URL = "https://api.steampowered.com"


class WebAPI:

    def __init__(self):
        self._session = requests.Session()

    def _request(self, method: str, endpoint: str, base_url: str = BASE_URL, **kwargs) -> requests.Response:
        """Makes a request to the Steam API."""
        url = f'{base_url}/{endpoint}'
        r = self._session.request(method, url, **kwargs)
        r.raise_for_status()
        return r

    def get_app_list(self) -> Dict[Any, Any]:
        """Returns a list of all Steam apps."""
        r = self._request('GET', 'ISteamApps/GetAppList/v2')
        return r.json()
