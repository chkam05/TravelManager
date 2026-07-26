from abc import ABC, abstractmethod
from typing import Any


class WebViewWindowInterface(ABC):
    """Defines the WebView window operations used by the application."""

    @abstractmethod
    def create(self) -> Any:
        """Creates and configures the native application window."""
        raise NotImplementedError

    @abstractmethod
    def start(self) -> None:
        """Starts the native WebView event loop."""
        raise NotImplementedError
