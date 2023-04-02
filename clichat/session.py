import os
import re
import glob
from clichat import storage


def list_sessions():
    """List names of sessions."""
    sess_paths = glob.glob(os.path.join(storage.get_cache_path(), "*.yaml"))
    return sorted(
        [
            re.sub("\.yaml\Z", "", os.path.basename(sess_path))  # noqa: W605
            for sess_path in sess_paths
        ]
    )


def delete_session(session):
    """Deletes a session.
    Returns None on success, error string otherwise"""
    session_path = storage.get_session_path(session, True)

    if not session_path:
        return f"session {session} does not exist"

    os.unlink(session_path)
