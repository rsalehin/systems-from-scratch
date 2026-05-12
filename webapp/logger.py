import logging
import os
from datetime import datetime

def setup_logger():
    # Create a logger named "webapp"
    logger = logging.getLogger("webapp")
    logger.setLevel(logging.DEBUG)

    # ── Format ────────────────────────────────────────────
    # Each log line looks like:
    # 2026-05-12 10:23:01 [INFO]  note created short_id=a3f9c1b2
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-8s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ── Handler 1: print to terminal ──────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # ── Handler 2: write to a file ────────────────────────
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    log_filename = os.path.join(logs_dir, "webapp.log")
    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # ── Attach both handlers ──────────────────────────────
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Module-level logger — import this anywhere
logger = setup_logger()