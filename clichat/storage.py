"""
Handles storage of cache and prompt config directories,
as well as figuring out where to put them on various platforms.
"""

import os
import yaml
import random
import string
import platformdirs
from clichat import chat, errors

APP_NAME = "clichat"


def get_cache_path(create=True):
    """
    If ~/.cache is available, always use ~/.cache/clichat as the cache file,
    otherwise revert to the platform's
    recommended location and create a directory.
    For example, ~/Library/Caches/clichat on osx.
    """
    os_cache_path = os.path.expanduser("~/.cache")
    if not os.path.exists(os_cache_path):
        os_cache_path = platformdirs.user_cache_dir(APP_NAME)
        if not os.path.exists(os_cache_path):
            os.makedirs(os_cache_path)

    cache_path = os.path.join(os_cache_path, APP_NAME)
    if create and not os.path.exists(cache_path):
        os.makedirs(cache_path)

    return cache_path


def get_session_path(session, exists=False):
    """
    Gets the path to the session file.
    If exists=True, return None if the path does not exist.
    """
    session_path = os.path.join(get_cache_path(), f"{session}.yaml")
    if exists and not os.path.exists(session_path):
        return
    return session_path


def messages_from_cache(session):
    """Loads messages from session.
    Return empty list if not exists.
    """
    file_path = get_session_path(session)
    if not os.path.exists(file_path):
        return []
    else:
        with open(file_path, "r") as f:
            return [chat.Message.import_yaml(m) for m in
                    yaml.load(f, yaml.SafeLoader)]


def load_prompt_config_legacy_yaml(prompt_name):
    """
    It is necessary to use YAML to load the configuration by its name.
    Assumes that the user created {name}.yaml in ~/.config/clichat
    """
    path = os.path.expanduser(
        os.path.join("~/.config/clichat", f"{prompt_name}.yaml")
    )
    try:
        with open(path, "r") as f:
            return yaml.load(f, Loader=yaml.FullLoader)["system"]
    except FileNotFoundError:
        raise errors.CliChatError(f"Prompt {prompt_name} not found in {path}")


def make_postfix():
    return "." + "".join(random.choices(string.ascii_letters + string.digits,
                                        k=10))


def load_prompt_file(prompt_name):
    """Loads the cue configuration by its name.
    Assumes that the user created the file ~/.config/clichat/{name_order} or
    the file directly in the path.
    """
    paths_to_try = [
        prompt_name,
        os.path.expanduser(os.path.join("~/.config/clichat",
                                        f"{prompt_name}")),
    ]
    try:
        for file_path in paths_to_try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    return f.read()
        # fallback legacy
        load_prompt_config_legacy_yaml(prompt_name)
    except Exception:
        locations = "".join(["\n - " + p for p in paths_to_try])
        raise errors.cliChat(
            f"no prompt {prompt_name} found in any of \
                following locations: {locations}"
        )
