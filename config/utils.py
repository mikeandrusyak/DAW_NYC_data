from typing import Iterable, List, Optional
import os   


def _clean(value: Optional[str]) -> Optional[str]:
    """Entfernt Inline-Kommentare (nach '#') und trimmt Whitespace."""
    if value is None:
        return None
    return value.split("#", 1)[0].strip()

def get_str(key: str, default: Optional[str] = None) -> Optional[str]:
    raw = os.getenv(key)
    val = _clean(raw)
    return val if (val is not None and val != "") else default

def get_int(key: str, default: Optional[int] = None) -> int:
    val = get_str(key)
    return int(val) if val is not None else default

def get_float(key: str, default: Optional[float] = None) -> float:
    val = get_str(key)
    return float(val) if val is not None else default

def get_bool(key: str, default: Optional[bool] = None) -> bool:
    val = get_str(key)
    if val is None:
        return default
    return val.lower() in {"true", "1", "yes", "on", "y"}

def get_list(
    key: str,
    sep: str = ",",
    strip_items: bool = True,
    default: Optional[Iterable[str]] = ()
) -> List[str]:
    """Komma-getrennte Liste parsen. Leere Items werden entfernt."""
    val = get_str(key)
    if val is None:
        return list(default)
    items = val.split(sep)
    if strip_items:
        items = [it.strip() for it in items]
    return [it for it in items if it != ""]

def validate(settings) -> None:
        # Beispielhafte Minimal-Validierungen
    if not settings.BASE_URL.startswith("http"):
        raise ValueError("BASE_URL muss mit http/https beginnen.")
    if settings.DEFAULT_SINCE > settings.DEFAULT_UNTIL:
        raise ValueError("DEFAULT_SINCE darf nicht größer als DEFAULT_UNTIL sein.")
    if settings.TARGET_SAMPLE <= 0:
        raise ValueError("TARGET_SAMPLE muss > 0 sein.")
    if settings.MAX_RETRIES < 0:
        raise ValueError("MAX_RETRIES darf nicht negativ sein.")
    if settings.TIMEOUT <= 0:
        raise ValueError("TIMEOUT muss > 0 sein.")
    if settings.DAYS_IN_MONTH <= 0 or settings.DAYS_IN_MONTH > 31:
        raise ValueError("DAYS_IN_MONTH sollte zwischen 1 und 31 liegen.")