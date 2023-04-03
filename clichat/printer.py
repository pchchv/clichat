import re
import sys
import json
import rich


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


def extract_messages(messages, args):
    message = messages[-1]
    if contains_json(message.content):
        print(extract_json(message.content))
    elif contains_block(message.content):
        print(extract_block(message.content))
    else:
        print(message.content.strip())
