import sys
import rich


def warn(msg):
    rich.print(f"[red]{msg}[/red]", file=sys.stderr)
