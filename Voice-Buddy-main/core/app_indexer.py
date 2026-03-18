import os
from pathlib import Path
from difflib import get_close_matches


class AppIndexer:
    def __init__(self):
        self.apps = {}
        self.index_apps()

    def index_apps(self):
        start_menu_dirs = [
            Path(os.environ["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs",
            Path(os.environ["PROGRAMDATA"]) / "Microsoft/Windows/Start Menu/Programs"
        ]

        for base in start_menu_dirs:
            for shortcut in base.rglob("*.lnk"):
                name = shortcut.stem.lower()
                if name not in self.apps:
                    self.apps[name] = shortcut

    def find(self, query: str):
        query = query.lower()

        # 1️⃣ Exact match
        if query in self.apps:
            return self.apps[query]

        # 2️⃣ Partial match
        for name, path in self.apps.items():
            if query in name:
                return path

        # 3️⃣ Fuzzy match
        matches = get_close_matches(
            query,
            self.apps.keys(),
            n=1,
            cutoff=0.6
        )

        if matches:
            return self.apps[matches[0]]

        return None
