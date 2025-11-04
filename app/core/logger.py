import logging
from pathlib import Path

def setup_logger(level=logging.INFO, log_dir="logs") -> logging.Logger:
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("library_app")
    logger.setLevel(level)

    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

    if not logger.handlers:
        handler = logging.FileHandler(log_path / "app.log")
        handler.setLevel(level)
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = setup_logger()