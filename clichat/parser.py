import os
import sys


def get_piped_input():
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None


def get_openai_key(options):
    if options["openai_api_key"]:
        return options["openai_api_key"]
    elif "OPENAI_API_KEY" in os.environ:
        return os.environ["OPENAI_API_KEY"]
    else:
        return None
