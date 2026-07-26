from __future__ import annotations
import json
import ssl
from typing import Any, ClassVar
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class MapDataDownloader:
    """Provides shared JSON transport for external map services."""

    USER_AGENT: ClassVar[str] = 'TravelManager/1.0'

    @classmethod
    def get_json(cls, url: str, timeout: int = 25) -> Any:
        """Loads JSON from an external URL."""
        request = Request(url, headers={
            'Accept': 'application/json',
            'User-Agent': cls.USER_AGENT
        })
        return cls._execute(request, timeout)

    @classmethod
    def get_json_with_params(cls, base_url: str, path: str, params: dict[str, Any]) -> Any:
        """Loads JSON using encoded query parameters."""
        return cls.get_json(f'{base_url}{path}?{urlencode(params)}')

    @classmethod
    def post_form_json(cls, url: str, data: dict[str, str], timeout: int = 14) -> Any:
        """Posts form data and returns decoded JSON."""
        request = Request(
            url,
            data=urlencode(data).encode('utf-8'),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'User-Agent': cls.USER_AGENT
            },
            method='POST'
        )
        return cls._execute(request, timeout)

    @classmethod
    def post_json(cls, url: str, data: dict[str, Any], timeout: int = 20) -> Any:
        """Posts a JSON payload and returns decoded JSON."""
        request = Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=utf-8',
                'User-Agent': cls.USER_AGENT
            },
            method='POST'
        )
        return cls._execute(request, timeout)

    @classmethod
    def _execute(cls, request: Request, timeout: int) -> Any:
        """Executes a request with the project's SSL compatibility fallback."""
        try:
            return cls._load_json(request, timeout=timeout)
        except URLError as error:
            if not isinstance(error.reason, ssl.SSLCertVerificationError):
                raise

            return cls._load_json(
                request,
                context=ssl._create_unverified_context(),
                timeout=timeout
            )

    @staticmethod
    def _load_json(
        request: Request,
        context: ssl.SSLContext | None = None,
        timeout: int = 25
    ) -> Any:
        """Executes a request and decodes its JSON body."""
        with urlopen(request, timeout=timeout, context=context) as response:
            return json.loads(response.read().decode('utf-8'))
