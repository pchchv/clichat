import re
import sys
import json
import rich
from clichat import utils
from rich.json import JSON
from rich.markdown import Markdown


def warn(msg):
    rich.print(f"[red]{msg}[/red]", file=sys.stderr)


def contains_json(str):
    try:
        extract_json(str)
    except ValueError:
        return False
    return True


def extract_json(str):
    """Attempts to extract JSON from a string that
    may contain other strings before JSON.
    Returns the JSON as a string or gives a
    ValueError if the JSON is not found.
    """
    lines_with_idxs = enumerate(str.splitlines())
    for idx, line in lines_with_idxs:
        if line.strip().startswith("{") or line.strip().startswith("["):
            return json.dumps(json.loads(" ".join(str.splitlines()[idx:])))

    raise ValueError("No json in string")


def contains_block(str):
    if extract_block(str):
        return True
    return False


def extract_block(str):
    matches = re.findall(r"```[\w]*(.*?)```", str, re.DOTALL)
    try:
        return sorted(matches, key=lambda x: len(x))[-1].strip()
    except IndexError:
        return None


def is_markdown(str):
    """Helps avoid marking up things that shouldn't be marking up."""
    md_links = len(re.findall(r"\[[^]]+\]\(https?:\/\/\S+\)", str))
    md_text = len(re.findall(r"\s(__|\*\*)(?!\s)(.(?!\1))+(?!\s(?=\1))", str))
    md_blocks = len(re.findall(r"```(.*?)```", str, re.DOTALL))
    md_inline_blocks = len(re.findall(r"`[^`]+`", str)) - md_blocks

    md_blocks *= 2
    utils.debug(
        title="counted",
        md_links=md_links,
        md_text=md_text,
        md_inline_blocks=md_inline_blocks,
        md_blocks=md_blocks,
    )

    return ((md_links + md_text + md_inline_blocks + md_blocks) >= 2)


def extract_messages(messages, args):
    message = messages[-1]
    if contains_json(message.content):
        print(extract_json(message.content))
    elif contains_block(message.content):
        print(extract_block(message.content))
    else:
        print(message.content.strip())


def detect_and_format_message(msg, cutoff=None):
    if cutoff and len(msg) > cutoff:
        msg = "... **text shortened** ... " + msg[-cutoff:]
        return msg
    elif contains_json(msg):
        utils.debug(detected="json")
        return JSON(extract_json(msg))
    elif is_markdown(msg):
        utils.debug(detected="markdown")
        return Markdown(msg)
    else:
        utils.debug(detected="regular")
        return msg
