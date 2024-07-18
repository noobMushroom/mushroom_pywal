"""
Reload programs.
"""
import logging
import os
import shutil
import subprocess

from .settings import CACHE_DIR, MODULE_DIR, OS
from . import util


def tty(tty_reload):
    """Load colors in tty."""
    tty_script = os.path.join(CACHE_DIR, "colors-tty.sh")
    term = os.environ.get("TERM")

    if tty_reload and term == "linux":
        subprocess.Popen(["sh", tty_script])


def xrdb(xrdb_files=None):
    """Merge the colors into the X db so new terminals use them."""
    xrdb_files = xrdb_files or \
        [os.path.join(CACHE_DIR, "colors.Xresources")]

    if shutil.which("xrdb") and OS != "Darwin":
        for file in xrdb_files:
            subprocess.run(["xrdb", "-merge", "-quiet", file], check=False)


def gtk():
    """Reload GTK theme on the fly."""
    gtk_reload = os.path.join(MODULE_DIR, "scripts", "gtk_reload.py")
    util.disown(["python3", gtk_reload])


def dwm():
    """Reload dwm colors"""
    if shutil.which("dwm") and util.get_pid("dwm"):
        if shutil.which("xrdb") and OS != "Darwin":
            file = os.path.join(CACHE_DIR, "dwm.xresources")
            subprocess.run(["xrdb", "-merge", "-quiet", file], check=False)
        if shutil.which("xsetroot") and util.get_pid("dwm"):
            util.disown(["xsetroot", "-name", "fsignal:1"])


def kitty():
    """ Reload kitty colors. """
    if (shutil.which("kitty")
            and util.get_pid("kitty")
            and os.getenv('TERM') == 'xterm-kitty'):
        subprocess.call([
            "kitty", "@", "set-colors", "--all",
            os.path.join(CACHE_DIR, "colors-kitty.conf")
        ])


def colors(cache_dir=CACHE_DIR):
    """Reload colors. (Deprecated)"""
    sequences = os.path.join(cache_dir, "sequences")

    logging.error("'wal -r' is deprecated: "
                  "Use 'cat %s' instead.", sequences)

    if os.path.isfile(sequences):
        print("".join(util.read_file(sequences)), end="")


def env(xrdb_file=None, tty_reload=True):
    """Reload environment."""
    xrdb(xrdb_file)
    kitty()
    dwm()
    logging.info("Reloaded environment.")
    tty(tty_reload)
