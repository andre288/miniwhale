from enum import Enum


class Severity(str, Enum):
    """ Levels of normalized severity"""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

    @classmethod
    def order(cls) -> dict["Severity", int]:
        return {cls.INFO: 0, cls.WARNING: 1, cls.ERROR: 2, cls.CRITICAL: 3}

    def __ge__(self, other: "Severity") -> bool:
        return Severity.order()[self] >= Severity.order()[other]
