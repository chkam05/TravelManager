from __future__ import annotations

from pathlib import Path
import shutil
from typing import Callable


class OfflineMapResourceError(RuntimeError):
    """Raised before a pipeline stage can exhaust local storage."""


class OfflineMapResourceGuard:
    MINIMUM_FREE_BYTES = 512 * 1024 * 1024
    WORKING_MULTIPLIER = 4

    def __init__(
        self, root: Path,
        disk_usage: Callable[[Path], object] = shutil.disk_usage,
    ):
        self.root = Path(root)
        self._disk_usage = disk_usage

    def available(self) -> int:
        return int(self._disk_usage(self.root).free)

    def required_for_download(self, source_size: int | None) -> int:
        if source_size is None or source_size <= 0:
            return self.MINIMUM_FREE_BYTES
        return max(self.MINIMUM_FREE_BYTES, source_size * self.WORKING_MULTIPLIER)

    def ensure(self, required: int, stage: str) -> None:
        available = self.available()
        required = max(self.MINIMUM_FREE_BYTES, int(required))
        if available < required:
            raise OfflineMapResourceError(
                f'Za mało miejsca na dysku dla etapu „{stage}”: '
                f'wymagane {required} B, dostępne {available} B.'
            )

    def ensure_download(self, source_size: int | None) -> None:
        self.ensure(self.required_for_download(source_size), 'pobieranie')

    def ensure_stage(self, artifact_size: int, stage: str, multiplier: int = 2) -> None:
        self.ensure(max(0, int(artifact_size)) * multiplier, stage)
