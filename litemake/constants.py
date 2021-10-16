""" Constant values that are used and shared across the litemake source code. """

import string

PACKAGE_CONFIG_FILENAME = "package.litemake.toml"
TARGETS_CONFIG_FILENAME = "targets.litemake.toml"
SETTINGS_FILENAME = "settings.litemake.toml"
CACHE_FOLDERNAME = ".litemake/"

SPECIAL_CHARS = "-_."
NAME_CHARS = string.ascii_letters + string.digits + SPECIAL_CHARS

VALID_HOOK_NAMES = {
    # plugin collection
    "after_collecting_plugins",
    # node collection
    "before_node_collection",
    "after_collecting_node",
    "after_node_collection",
    # node compilation
    "before_node_compilation",
    "before_compiling_node",
    "after_compiling_node",
    "after_node_compilation",
}


PLUGINS_ENTRY_POINT = "litemake-plugins"
