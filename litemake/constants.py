""" Constant values that are used and shared across the litemake source code. """

import string

PACKAGE_CONFIG_FILENAME = "package.litemake.toml"
TARGETS_CONFIG_FILENAME = "targets.litemake.toml"
SETTINGS_FILENAME = "settings.litemake.toml"
CACHE_FOLDERNAME = ".litemake/"

SPECIAL_CHARS = "-_."
NAME_CHARS = string.ascii_letters + string.digits + SPECIAL_CHARS
