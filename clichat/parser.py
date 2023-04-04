import os
import sys
import argparse
from clichat import utils


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


def extract_query(query):
    """
    Generates a query from a query as well as from any pipeline input.
    The user can provide either only the query or the pipeline input,
    or both, in which case the pipeline input is placed above the query.
    """
    query = " ".join(query) if query else None

    piped_input = get_piped_input()
    if query and piped_input:
        return piped_input + "\n----------------\n" + query
    elif query:
        return query
    elif piped_input:
        return piped_input
    else:
        return None


def extract_options(options):
    options = vars(options)  # to map
    options["openai_api_key"] = get_openai_key(options)
    options["model"] = {"3.5": "gpt-3.5-turbo", "4": "gpt-4"}[options["chat_gpt"]]
    del options["query"]
    del options["chat_gpt"]

    return utils.DotDict(options)


def valid_session(sess):
    if all(char not in sess for char in ["/", "\\", "\n"]):
        return sess
    else:
        raise argparse.ArgumentTypeError(f"invalid session name {sess}")
