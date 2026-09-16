class OfflineMapProcessingCancelled(RuntimeError):
    """Base exception for a user-cancelled offline-map pipeline stage."""


class OfflineMapDownloadError(RuntimeError):
    pass


class OfflineMapDownloadCancelled(
    OfflineMapProcessingCancelled, OfflineMapDownloadError
):
    pass


class OfflineMapAnalysisError(RuntimeError):
    pass


class OfflineMapAnalysisCancelled(
    OfflineMapProcessingCancelled, OfflineMapAnalysisError
):
    pass


class OfflineMapTileGenerationError(RuntimeError):
    pass


class OfflineMapTileGenerationCancelled(
    OfflineMapProcessingCancelled, OfflineMapTileGenerationError
):
    pass


class OfflineMapInstallationError(RuntimeError):
    pass


class OfflineMapInstallationCancelled(
    OfflineMapProcessingCancelled, OfflineMapInstallationError
):
    pass
