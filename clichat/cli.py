import os
from clichat import storage, utils, printer


def migrate_old_cache_file_if_exists():
    cache_path = storage.get_cache_path()

    if os.path.isfile(cache_path):
        try:
            storage.migrate_to_session(utils.scratch_session)
        except Exception as e:
            printer.warn(f"failed to migrate old cache file: {e}")
            return 1
