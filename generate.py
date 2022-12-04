# https://github.com/SchnoppDog/Advent-of-Code-Collection/blob/main/create_file_structure.py
import logging
import os
from pathlib import Path

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger(__name__)


def create_file_structure(_root: str, dry_run=False):
    """Creates my file structure for advent of code
    Args:
        abspath (str): Absolute path where the new AoC directory should be created.
        dirname (str): The name of the AoC root directory.
        src_dirname (str): The name where to create the day-dirs and files.
    """
    root = Path(_root).resolve()
    if not root.is_dir():
        raise Exception(f"{root} is not a directory")
    logger.info("Using '%s'", root)
    for d in range(1, 26):
        _d_dir = "d{:02d}".format(d)
        d_dir = root / _d_dir
        if d_dir.is_dir():
            logger.info("Already exists: '%s'", _d_dir)
            continue
        logger.info("Creating '%s'", d_dir)
        if not dry_run:
            d_dir.mkdir(mode=0o755)
            (d_dir / "main.py").touch(mode=0o644)
            (d_dir / "test.py").touch(mode=0o644)
            (d_dir / "main.ipynb").touch(mode=0o644)
