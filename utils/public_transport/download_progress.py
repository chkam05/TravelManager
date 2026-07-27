from __future__ import annotations
from contextlib import contextmanager
from contextvars import ContextVar
from time import sleep
from typing import Callable, ClassVar, Iterator, TypeVar


T = TypeVar('T')
ProgressCallback = Callable[[str, int, int, int, int], None]


class PublicTransportDownloadProgress:
    """Reports public transport downloads and retries individual operations."""

    MAX_ATTEMPTS: ClassVar[int] = 3
    _CALLBACK: ClassVar[ContextVar[ProgressCallback | None]] = ContextVar(
        'public_transport_progress_callback',
        default=None
    )

    def __new__(cls):
        """Prevents creating instances of this shared utility class."""
        raise TypeError(f'{cls.__name__} cannot be instantiated.')

    #region Context

    @classmethod
    @contextmanager
    def bind(cls, callback: ProgressCallback) -> Iterator[None]:
        """Binds a progress receiver to the current request context."""
        token = cls._CALLBACK.set(callback)
        try:
            yield
        finally:
            cls._CALLBACK.reset(token)

    #endregion Context

    #region Progress and retry

    @classmethod
    def report(
        cls,
        item: str,
        current: int = 1,
        total: int = 1,
        attempt: int = 1,
        max_attempts: int | None = None
    ) -> None:
        """Reports the currently downloaded item and retry attempt."""
        callback = cls._CALLBACK.get()
        if callback:
            callback(
                item,
                max(0, current),
                max(0, total),
                max(1, attempt),
                max_attempts or cls.MAX_ATTEMPTS
            )

    @classmethod
    def retry(
        cls,
        operation: Callable[[], T],
        item: str,
        current: int = 1,
        total: int = 1,
        max_attempts: int | None = None
    ) -> T:
        """Executes one download at most three times and reports every attempt."""
        attempts = min(
            cls.MAX_ATTEMPTS,
            max(1, max_attempts or cls.MAX_ATTEMPTS)
        )
        last_error: Exception | None = None
        for attempt in range(1, attempts + 1):
            cls.report(item, current, total, attempt, attempts)
            try:
                return operation()
            except Exception as error:
                last_error = error
                if attempt < attempts:
                    sleep(0.2 * attempt)
        raise last_error or RuntimeError(f'Nie udało się pobrać: {item}')

    #endregion Progress and retry
