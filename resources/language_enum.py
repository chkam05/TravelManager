from enum import StrEnum


class Language(StrEnum):
    """Locales supported by the application."""

    ENGLISH = 'en_US'
    POLISH = 'pl_PL'

    @property
    def label_key(self) -> str:
        """Returns the translation key used by language selectors."""
        return f'SETTINGS_APPLICATION.LANGUAGE_{self.name}'

    @property
    def cli_code(self) -> str:
        """Returns the short language code accepted by the CLI."""
        return self.value.partition('_')[0].upper()
