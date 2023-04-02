"""
Handles storage of cache and prompt config directories,
as well as figuring out where to put them on various platforms.
"""

import os
import platformdirs

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
