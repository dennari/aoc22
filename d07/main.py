import logging
import os
import re
from typing import Dict, Optional, Self

logging.basicConfig()
logger = logging.getLogger()

dir_path = os.path.dirname(os.path.realpath(__file__))


class Node:
    name: str
    type: str
    size: Optional[int]
    children: Dict[str, Self]

    def __init__(
        self,
        name: str,
        type: str,
        size: Optional[int] = None,
    ):
        self.name = name
        self.type = type
        self.size = size
        # WTF: if I set this as a constructor _default_ argument, everything breaks
        self.children = {}


command_re = re.compile(r"[\$\s]*(\w+)(\s+(.+))?")
ls_re = re.compile(r"([^\s]+)\s+(.+)")


def parse_command(s: str):
    m = command_re.match(s)
    return m.group(1), m.group(3)


def parse_ls_output(s: str):
    m = ls_re.match(s)
    return m.group(1), m.group(2)


def read_command(filename=dir_path + "/input.txt"):
    with open(filename) as f:
        current_command = None
        current_output = None
        while len(line := f.readline().strip()) > 0:
            if line[0] == "$":
                if current_command is not None:
                    yield current_command, current_output
                    current_command = None
                    current_output = None
                current_command = parse_command(line)
            elif current_command and current_command[0] == "ls":
                if current_output is None:
                    current_output = []
                current_output.append(parse_ls_output(line))
            else:
                raise Exception("Unknown output")
        if current_command is not None:
            yield current_command, current_output


def build():
    root = None
    current = None
    files = []
    dirs = []
    stack = []
    max_depth = 0
    for c, o in read_command():
        match c:
            case ("cd", ".."):
                stack.pop()
                current = stack[-1]
                logger.info("CD .., %s, %d, %s", current.name, len(current.children), c)
            case ("cd", dn):
                if current:
                    if dn in current.children:
                        msg = "FOUND"
                        node = current.children[dn]
                    else:
                        raise Exception(f"Unknown: {dn}")
                else:
                    msg = "NO_CURRENT"
                    node = Node(name=dn, type="D", size=None)
                current = node
                logger.info("CD %s, %s, %d %s", dn, msg, len(current.children), c)

                stack.append(node)
                if (sl := len(stack)) > max_depth:
                    max_depth = sl
                if dn == "/":
                    dirs.append("/")
                    root = node
            case ("ls", *_):
                if current is None:
                    raise Exception("No CWD")
                logger.info(
                    "LS %s, %d -> %d", current.name, len(current.children), len(o)
                )
                node = None
                for n in o:
                    match n:
                        case ("dir", dn):
                            node = Node(name=dn, type="D", size=None)
                            dirs.append(dn)
                        case (fs, fn):
                            node = Node(name=fn, type="F", size=int(fs))
                            files.append(fn)
                        case _:
                            raise Exception("Unknown output")
                    if node.name in current.children:
                        raise Exception(f"{current.name}: duplicate node {node.name}")
                    current.children[node.name] = node

            case _:
                raise Exception("Unknown command")
    return root, files, dirs, max_depth


def get_sizes(root: Node):
    sizes = []
    depths = []

    def get_size(n: Node, depth: int):
        # print(n.type, n.size, len(n.children))
        if n.type == "F":
            # print(depth)
            return n.size
        size = sum(get_size(c, depth + 1) for c in n.children.values())
        sizes.append(size)
        depths.append(depth)
        return size

    get_size(root, 0)
    return sizes
