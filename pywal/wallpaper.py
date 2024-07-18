"""Set the wallpaper."""
import logging
import os
import shutil

from .settings import CACHE_DIR
from . import util


def set_wm_wallpaper(img):
    """Set the wallpaper for non desktop environments."""
    if shutil.which("feh"):
        util.disown(["feh", "--bg-fill", img])


def change(img):
    """Set the wallpaper."""
    set_wm_wallpaper(img)
    logging.info("Set the new wallpaper.")


def get(cache_dir=CACHE_DIR):
    """Get the current wallpaper."""
    current_wall = os.path.join(cache_dir, "wal")

    if os.path.isfile(current_wall):
        return util.read_file(current_wall)[0]

    return "None"
