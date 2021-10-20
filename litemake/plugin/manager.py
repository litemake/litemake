import inspect

from .hook import Hook


class litemakePluginManager:
    """An internal singleton object that shouldn't be exposed or accessed by
    third-party plugins, that stores those plugins and activates differnet
    hooks."""

    def __init__(self, *plugins):
        self._plugins = plugins

    @staticmethod
    def __does_method_exist(instance: object, method_name: str) -> bool:
        """Returns True if the given instance has a method with the given name.
        Used to check if a plugin has a registered hook."""
        members = {name: value for name, value in inspect.getmembers(instance)}
        return method_name in members and inspect.ismethod(members[method_name])

    def __getattr__(self, name: str):
        funcs = [
            # Collect functions list only functions that registered to this hook
            plugin.__getattribute__(name)
            for plugin in self._plugins
            if self.__does_method_exist(plugin, name)
        ]

        return Hook(*funcs)
