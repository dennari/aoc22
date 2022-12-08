# import pytest
import logging

from .main import build, get_sizes, read_command

logging.basicConfig()
logger = logging.getLogger()


def test_read_command():
    files = []
    dirs = []
    for c, o in read_command():
        if c[0] == "cd" and c[1] != "..":
            dirs.append(c[1])
    logger.info("DIRS all: %d, unique: %d", len(dirs), len(set(dirs)))
    dirs = []
    for c, o in read_command():
        if c[0] == "ls":
            for n in o:
                if n[0] == "dir":
                    dirs.append(n[1])
                else:
                    files.append(n[1])
    logger.info("DIRS all: %d, unique: %d", len(dirs), len(set(dirs)))
    logger.info("FILES all: %d, unique: %d", len(files), len(set(files)))


def test_build():
    root, files, dirs, max_depth = build()
    assert len(files) == 290
    assert len(set(files)) == 200
    assert len(dirs) == 194
    assert len(set(dirs)) == 148
    logger.info("max_depth: %d", max_depth)
    logger.info("all: %d, unique: %d", len(files), len(set(files)))
    logger.info("all: %d, unique: %d", len(dirs), len(set(dirs)))


def test_get_sizes():
    root, files, dirs, max_depth = build()
    sizes = get_sizes(root)
    sizes_s = list(x for x in sizes if x <= 100000)
    logger.info(sizes_s)
    # PART 1
    logger.info(sum(sizes_s))


def test_free_space():
    root, files, dirs, max_depth = build()
    total_space = 70000000
    need_free = 30000000
    sizes = get_sizes(root)
    used = sizes[-1]
    current_free = total_space - used
    delete_at_least = need_free - current_free
    logger.info("delete_at_least: %d", delete_at_least)
    candidate = min(x for x in sizes if x >= delete_at_least)
    logger.info(candidate)
