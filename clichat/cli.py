import os
import types
from rich.text import Text
from rich.live import Live
from clichat import storage, utils, printer, session, chat


def migrate_old_cache_file_if_exists():
    cache_path = storage.get_cache_path()

    if os.path.isfile(cache_path):
        try:
            storage.migrate_to_session(utils.scratch_session)
        except Exception as e:
            printer.warn(f"failed to migrate old cache file: {e}")
            return 1


def do_session_op(sess, op, rename_to):
    if op == "list":
        print(*session.list(), sep="\n")
        return 0

    err = None
    if not sess:
        err = "session name required"
    elif op == "path" or op == "dump":
        sess_path = storage.get_session_path(sess, True)
        if sess_path:
            if op == "path":
                data = sess_path
            else:
                with open(sess_path, "r") as f:
                    data = f.read()
            print(data)
        else:
            err = "session does not exist"
    elif op == "delete":
        err = session.delete(sess)
    elif op == "rename":
        err = session.rename(sess, rename_to)
    else:
        raise ValueError(f"unknown session operation: {op}")

    if err:
        printer.warn(err)
        return 1

    return 0


def fetch_and_cache(messages, params):
    result = chat.query_chatgpt(messages, params)
    if isinstance(result, types.GeneratorType):
        text = Text("")
        message = None
        with Live(text, refresh_per_second=4) as live:
            for message in result:
                live.update(message.content)
            live.update("")
        response_msg = message
    else:
        response_msg = chat.query_chatgpt(messages, params)
    messages.append(response_msg)
    storage.to_cache(messages, params.session or utils.scratch_session)
    return messages
