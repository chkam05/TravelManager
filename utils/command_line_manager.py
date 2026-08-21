from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from typing import ClassVar

from core.language_service import LanguageService
from resources.language_enum import Language
from storage.settings_storage import SettingsStorage
from utils.network_utils import NetworkUtils


class CommandLineManager:
    """Builds and validates the command line interface."""

    LANGUAGE_LOCALES: ClassVar[dict[str, str]] = {
        language.cli_code: language.value for language in Language
    }
    _LANGUAGE_SERVICE: ClassVar[LanguageService] = LanguageService()

    @classmethod
    def language_locale(cls, language: str | None) -> str | None:
        """Maps a supported command-line language code to an app locale."""
        return cls.LANGUAGE_LOCALES.get(language) if language is not None else None

    @classmethod
    def configured_locale(cls) -> str:
        """Returns the persisted locale used by command-line messages."""
        try:
            locale = SettingsStorage().load().ui.language
            return LanguageService.normalize_locale(locale)
        except (OSError, TypeError, ValueError):
            return LanguageService.DEFAULT_LOCALE

    @classmethod
    def translate(
        cls,
        key: str,
        locale: str | None = None,
        **parameters: object
    ) -> str:
        """Translates a message outside a Flask request context."""
        return cls._LANGUAGE_SERVICE.translate(
            key,
            locale=locale or cls.configured_locale(),
            parameters=parameters
        )

    @classmethod
    def ipv4_argument(cls, value: str, locale: str | None = None) -> str:
        """Validates an IPv4 command-line argument."""
        try:
            return NetworkUtils.normalize_ipv4(value)
        except (TypeError, ValueError) as error:
            raise argparse.ArgumentTypeError(
                cls.translate(str(error), locale, value=value)
            ) from error

    @classmethod
    def port_argument(cls, value: str, locale: str | None = None) -> int:
        """Validates a TCP port command-line argument."""
        try:
            port = int(value)
        except ValueError as error:
            raise argparse.ArgumentTypeError(
                cls.translate('CLI.PORT_MUST_BE_INTEGER', locale)
            ) from error

        if not 1 <= port <= 65535:
            raise argparse.ArgumentTypeError(
                cls.translate('CLI.PORT_OUT_OF_RANGE', locale)
            )

        return port

    @classmethod
    def create_argument_parser(
        cls,
        locale: str | None = None
    ) -> argparse.ArgumentParser:
        """Creates a parser supporting Unix and Windows-style options."""
        selected_locale = LanguageService.normalize_locale(
            locale or cls.configured_locale()
        )
        parser = argparse.ArgumentParser(
            description=cls.translate('CLI.DESCRIPTION', selected_locale),
            add_help=False,
            prefix_chars='-/'
        )
        parser.add_argument(
            '--ip', '/ip',
            type=lambda value: cls.ipv4_argument(value, selected_locale),
            help=cls.translate('CLI.IP_HELP', selected_locale)
        )
        parser.add_argument(
            '--port', '/port',
            type=lambda value: cls.port_argument(value, selected_locale),
            help=cls.translate('CLI.PORT_HELP', selected_locale)
        )
        parser.add_argument(
            '--lang', '/lang',
            choices=tuple(cls.LANGUAGE_LOCALES),
            dest='language',
            help=cls.translate('CLI.LANG_HELP', selected_locale)
        )
        parser.add_argument(
            '--no-window', '/no-window',
            action='store_true',
            help=cls.translate('CLI.NO_WINDOW_HELP', selected_locale)
        )
        parser.add_argument(
            '-h', '--help', '/h', '/help',
            action='help',
            help=cls.translate('CLI.HELP', selected_locale)
        )
        return parser

    @classmethod
    def parse_arguments(
        cls,
        arguments: Sequence[str] | None = None
    ) -> argparse.Namespace:
        """Parses options and localizes help using the requested language."""
        bootstrap_parser = argparse.ArgumentParser(
            add_help=False,
            prefix_chars='-/'
        )
        bootstrap_parser.add_argument(
            '--lang', '/lang',
            choices=tuple(cls.LANGUAGE_LOCALES),
            dest='language'
        )
        known_arguments, _ = bootstrap_parser.parse_known_args(arguments)
        locale = cls.language_locale(known_arguments.language)
        return cls.create_argument_parser(locale).parse_args(arguments)

    @staticmethod
    def prepare_console() -> None:
        """Attaches windowed builds to a terminal when CLI options are used."""
        if len(sys.argv) <= 1 or (sys.stdout is not None and sys.stderr is not None):
            return

        if sys.platform == 'win32':
            try:
                import ctypes

                kernel32 = ctypes.windll.kernel32
                if not kernel32.AttachConsole(-1):
                    kernel32.AllocConsole()
                kernel32.SetConsoleCtrlHandler(None, False)
                sys.stdin = open('CONIN$', 'r', encoding='utf-8')
                sys.stdout = open('CONOUT$', 'w', encoding='utf-8', buffering=1)
                sys.stderr = open('CONOUT$', 'w', encoding='utf-8', buffering=1)
            except (OSError, AttributeError):
                return
            return

        try:
            sys.stdin = open('/dev/tty', 'r', encoding='utf-8')
            sys.stdout = open('/dev/tty', 'w', encoding='utf-8', buffering=1)
            sys.stderr = open('/dev/tty', 'w', encoding='utf-8', buffering=1)
        except OSError:
            return
