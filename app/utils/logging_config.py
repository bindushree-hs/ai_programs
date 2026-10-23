"""Standard-library logging configuration."""

import logging


def configure_logging() -> None:
    """Configure concise application logs without sensitive payloads."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
