import json
import os

DEFAULT_FORMAT = {"maps": {}, "players": {}, "teams": {}}


class AliasNotFoundError(Exception):
    def __init__(self, alias_type: str, alias: str):
        self.alias_type = alias_type
        self.alias = alias


class Aliases:
    def __init__(self, filename="aliases.json"):
        self._filename = filename
        self._aliases = {}
        self.AliasNotFoundError = AliasNotFoundError
        if not os.path.isfile(filename):
            with open(filename, "w") as file:
                json.dump(DEFAULT_FORMAT, file)
        with open(filename) as file:
            data = json.load(file)
            self._aliases = data

    def get(self, alias_type: str, name: str):
        data = self._aliases.get(alias_type, {})
        alias = data.get(name)
        if alias is None:
            for key in data.keys():
                if key.lower() == name.lower():
                    alias = data.get(key)
                    break
            else:
                raise AliasNotFoundError(alias_type, name)
        return alias

    def get_map(self, name: str):
        return self.get("maps", name)

    def get_player(self, name: str):
        return self.get("players", name)

    def get_team(self, name: str):
        return self.get("teams", name)