from dataclasses import dataclass
from functools import lru_cache
from dotenv import load_dotenv
from pathlib import Path
from .utils import get_bool, get_float, get_int, get_list, get_str, validate


# .env laden (liegt standardmäßig neben config.py; passe an, wenn nötig)
ENV_PATH = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=ENV_PATH if ENV_PATH.exists() else None, override=True)


@dataclass(frozen=True)
class Settings:
    BASE_URL: str
    DEFAULT_SINCE: int
    DEFAULT_UNTIL: int
    TARGET_SAMPLE: int
    MAX_RETRIES: int
    TIMEOUT: float
    BASE_DELAY: float
    GROUP_BY: str
    GROUP_BY_VALUE: list[str]
    DAYS_IN_MONTH: int
    SLEEP_FOR_SECONDS: float
    PLOT_DIST: bool
        
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings(
        BASE_URL=get_str("BASE_URL"),
        DEFAULT_SINCE=get_int("DEFAULT_SINCE"),
        DEFAULT_UNTIL=get_int("DEFAULT_UNTIL"),
        TARGET_SAMPLE=get_int("TARGET_SAMPLE"),
        MAX_RETRIES=get_int("MAX_RETRIES"),
        TIMEOUT=get_int("TIMEOUT"),
        BASE_DELAY=get_float("BASE_DELAY"),
        GROUP_BY=get_str("GROUP_BY"),
        GROUP_BY_VALUE=get_list(
            "GROUP_BY_VALUE",
            default=("BRONX", "BROOKLYN", "MANHATTAN", "QUEENS", "STATEN ISLAND", "Unspecified"),
        ),
        DAYS_IN_MONTH=get_int("DAYS_IN_MONTH"),
        SLEEP_FOR_SECONDS=get_float("SLEEP_FOR_SECONDS"),
        PLOT_DIST=get_bool("PLOT_DIST", False),
    )
    validate(settings)
    return settings