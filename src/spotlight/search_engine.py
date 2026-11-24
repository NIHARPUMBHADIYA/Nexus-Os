"""
NEXUS OS — Universal Spotlight Search Engine Core
High-performance modular search engine featuring SQLite FTS5, fuzzy matching,
usage-based ranking, sensitive file exclusions, and secure action execution.
"""

import os
import sys
import re
import json
import sqlite3
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

# Default exclusions for sensitive credentials and heavy build directories
SENSITIVE_EXTENSIONS = {
    ".pem", ".key", ".pfx", ".p12", ".crt", ".kdbx", ".env", ".token"
}

SENSITIVE_FILENAMES = {
    ".env", ".env.local", ".env.production", "id_rsa", "id_ed25519",
    "id_ecdsa", "credentials.json", "token.txt", "secrets.yaml", "vault.key"
}

DEFAULT_EXCLUDED_DIRS = {
    ".git", "node_modules", "target", "dist", "build", ".ssh",
    ".gnupg", "__pycache__", ".venv", "venv", ".idea", ".vscode"
}

# High-risk destructive command patterns requiring explicit confirmation
DESTRUCTIVE_PATTERNS = [
    re.compile(r"\brm\s+-[rf]+", re.IGNORECASE),
    re.compile(r"\bdd\s+if=", re.IGNORECASE),
    re.compile(r"\bmkfs\b", re.IGNORECASE),
    re.compile(r"\bshutdown\b", re.IGNORECASE),
    re.compile(r"\breboot\b", re.IGNORECASE),
    re.compile(r"\bpoweroff\b", re.IGNORECASE),
    re.compile(r"\bkill\s+-9\b", re.IGNORECASE),
    re.compile(r"\bsystemctl\s+(stop|disable|mask)\b", re.IGNORECASE)
]


class SearchResult:
    def __init__(self, item_id: str, title: str, description: str, category: str,
                 icon: str = "🔍", score: float = 0.0, metadata: Optional[Dict[str, Any]] = None,
                 actions: Optional[List[Dict[str, Any]]] = None):
        self.id = item_id
        self.title = title
        self.description = description
        self.category = category
        self.icon = icon
        self.score = score
        self.metadata = metadata or {}
        self.actions = actions or [
            {"id": "open", "title": "Open", "shortcut": "Enter", "destructive": False}
        ]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "icon": self.icon,
            "score": self.score,
            "metadata": self.metadata,
            "actions": self.actions
        }


class SearchProvider(ABC):
    @property
    @abstractmethod
    def category_name(self) -> str:
        pass

    @abstractmethod
    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        pass

    def get_actions(self, result: SearchResult) -> List[Dict[str, Any]]:
        return result.actions


# -----------------------------------------------------------------------------
# SQLite FTS5 Index Database
# -----------------------------------------------------------------------------
class SearchDatabase:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            cache_dir = os.path.expanduser("~/.cache/nexus")
            os.makedirs(cache_dir, exist_ok=True)
            self.db_path = os.path.join(cache_dir, "spotlight.db")
        else:
            self.db_path = db_path

        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            # Metadata & Full Text Search Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id TEXT PRIMARY KEY,
                    category TEXT,
                    title TEXT,
                    description TEXT,
                    path TEXT,
                    content TEXT,
                    metadata_json TEXT
                )
            """)
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS items_fts USING fts5(
                    title,
                    description,
                    content,
                    content='items',
                    content_rowid='rowid'
                )
            """)
            # Usage tracking for frequency and recency boost
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usage_history (
                    item_id TEXT PRIMARY KEY,
                    launch_count INTEGER DEFAULT 0,
                    last_launched REAL DEFAULT 0
                )
            """)
            # Configuration settings
            conn.execute("""
                CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            conn.commit()

    def insert_or_update(self, item_id: str, category: str, title: str,
                         description: str, path: str = "", content: str = "",
                         metadata: Optional[Dict[str, Any]] = None):
        meta_str = json.dumps(metadata or {})
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO items (id, category, title, description, path, content, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (item_id, category, title, description, path, content, meta_str))
            # Keep FTS5 in sync
            conn.execute("""
                INSERT OR REPLACE INTO items_fts(rowid, title, description, content)
                SELECT rowid, title, description, content FROM items WHERE id = ?
            """, (item_id,))
            conn.commit()

    def query_fts(self, query: str, category: Optional[str] = None, limit: int = 15) -> List[Dict[str, Any]]:
        clean_query = re.sub(r"[^\w\s]", "", query).strip()
        if not clean_query:
            return []

        fts_pattern = f'"{clean_query}"* OR {clean_query}*'
        with self._get_connection() as conn:
            try:
                if category and category != "All":
                    sql = """
                        SELECT i.id, i.category, i.title, i.description, i.path, i.metadata_json,
                               COALESCE(u.launch_count, 0) as launch_count,
                               COALESCE(u.last_launched, 0) as last_launched
                        FROM items i
                        JOIN items_fts f ON i.rowid = f.rowid
                        LEFT JOIN usage_history u ON i.id = u.item_id
                        WHERE items_fts MATCH ? AND i.category = ?
                        LIMIT ?
                    """
                    cursor = conn.execute(sql, (fts_pattern, category, limit))
                else:
                    sql = """
                        SELECT i.id, i.category, i.title, i.description, i.path, i.metadata_json,
                               COALESCE(u.launch_count, 0) as launch_count,
                               COALESCE(u.last_launched, 0) as last_launched
                        FROM items i
                        JOIN items_fts f ON i.rowid = f.rowid
                        LEFT JOIN usage_history u ON i.id = u.item_id
                        WHERE items_fts MATCH ?
                        LIMIT ?
                    """
                    cursor = conn.execute(sql, (fts_pattern, limit))
                return [dict(row) for row in cursor.fetchall()]
            except sqlite3.OperationalError:
                return []

    def record_usage(self, item_id: str):
        now = time.time()
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO usage_history (item_id, launch_count, last_launched)
                VALUES (?, 1, ?)
                ON CONFLICT(item_id) DO UPDATE SET
                    launch_count = launch_count + 1,
                    last_launched = ?
            """, (item_id, now, now))
            conn.commit()

    def get_stats(self) -> Dict[str, Any]:
        with self._get_connection() as conn:
            total_items = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
            categories = conn.execute("SELECT category, COUNT(*) FROM items GROUP BY category").fetchall()
            return {
                "total_indexed": total_items,
                "categories": {row[0]: row[1] for row in categories}
            }

    def clear_index(self):
        with self._get_connection() as conn:
            conn.execute("DELETE FROM items")
            conn.execute("DELETE FROM items_fts")
            conn.commit()


# -----------------------------------------------------------------------------
# Providers Implementation
# -----------------------------------------------------------------------------

class ApplicationProvider(SearchProvider):
    @property
    def category_name(self) -> str:
        return "Applications"

    def __init__(self):
        self.apps = [
            SearchResult("app:terminal", "Nexus Terminal", "Default Zsh / Starship terminal emulator", "Applications", "⌨",
                         actions=[
                             {"id": "open", "title": "Launch Terminal", "shortcut": "Enter"},
                             {"id": "new_window", "title": "Open New Window", "shortcut": "Ctrl+N"}
                         ]),
            SearchResult("app:devhub", "Developer Hub", "Project orchestrator, container runtimes & git status", "Applications", "📁",
                         actions=[{"id": "open", "title": "Launch Developer Hub", "shortcut": "Enter"}]),
            SearchResult("app:editor", "Code Editor", "High-performance developer text & code editor", "Applications", "💻",
                         actions=[{"id": "open", "title": "Launch Editor", "shortcut": "Enter"}]),
            SearchResult("app:aicore", "Nexus AI Core Manager", "Manage local Ollama models and unified proxy", "Applications", "🤖",
                         actions=[{"id": "open", "title": "Open AI Core", "shortcut": "Enter"}]),
            SearchResult("app:settings", "System Settings", "Configure appearance, themes, displays, shortcuts", "Applications", "⚙",
                         actions=[{"id": "open", "title": "Open Settings", "shortcut": "Enter"}]),
            SearchResult("app:browser", "Web Browser", "Wayland-native developer web browser", "Applications", "🌐",
                         actions=[{"id": "open", "title": "Launch Browser", "shortcut": "Enter"}])
        ]

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        q = query.lower().strip()
        results = []
        for app in self.apps:
            score = 0
            t_lower = app.title.lower()
            d_lower = app.description.lower()
            words = t_lower.split()
            if t_lower == q:
                score = 1000
            elif t_lower.startswith(q):
                score = 800
            elif any(w == q for w in words):
                score = 750
            elif any(w.startswith(q) for w in words):
                score = 700
            elif q in t_lower:
                score = 600
            elif q in d_lower:
                score = 400

            if score > 0:
                app_copy = SearchResult(app.id, app.title, app.description, app.category,
                                        app.icon, score, app.metadata, app.actions)
                results.append(app_copy)

        return results[:limit]


class ProjectProvider(SearchProvider):
    @property
    def category_name(self) -> str:
        return "Projects"

    def __init__(self, workspace_roots: Optional[List[str]] = None):
        self.workspace_roots = workspace_roots or [
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        ]

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        q = query.lower().strip()
        
        # Connect to DevHub registry if available
        projects = []
        try:
            from ..devhub.hub_core import get_hub
            hub = get_hub()
            hub_projects = hub.get_projects()
            for hp in hub_projects:
                projects.append({
                    "id": hp.get("id", "proj:unknown"),
                    "title": hp.get("name", "Project"),
                    "path": hp.get("path", ""),
                    "type": hp.get("language", "General"),
                    "branch": hp.get("git", {}).get("branch", "main")
                })
        except Exception:
            projects = [
                {
                    "id": "proj:nexus-os",
                    "title": "nexus-os",
                    "path": "d:/My own os",
                    "type": "Rust / Qt6",
                    "branch": "main (clean)"
                },
                {
                    "id": "proj:ai-agent-core",
                    "title": "ai-agent-core",
                    "path": "~/Projects/ai-agent-core",
                    "type": "Python / PyTorch",
                    "branch": "feature/tool-calling"
                },
                {
                    "id": "proj:robotics-nav2",
                    "title": "robotics-nav2",
                    "path": "~/Projects/robotics-nav2",
                    "type": "C++ / ROS 2",
                    "branch": "humble"
                }
            ]

        results = []
        for p in projects:
            score = 0
            name = p["title"].lower()
            if name == q:
                score = 950
            elif name.startswith(q):
                score = 750
            elif q in name or q in p["type"].lower():
                score = 550

            if score > 0:
                actions = [
                    {"id": "open_ide", "title": "Open in Code Editor", "shortcut": "Enter"},
                    {"id": "terminal_here", "title": "Open Terminal Here", "shortcut": "Ctrl+T"},
                    {"id": "reveal", "title": "Reveal in Files", "shortcut": "Ctrl+R"},
                    {"id": "copy_path", "title": "Copy Path", "shortcut": "Ctrl+C"}
                ]
                desc = f"{p['type']} • {p['branch']} • {p['path']}"
                results.append(SearchResult(p["id"], p["title"], desc, "Projects", "📁", score,
                                            metadata={"path": p["path"]}, actions=actions))
        return results[:limit]


class FileProvider(SearchProvider):
    @property
    def category_name(self) -> str:
        return "Files"

    def is_safe_path(self, path: str) -> bool:
        basename = os.path.basename(path).lower()
        ext = os.path.splitext(path)[1].lower()

        # Reject credentials and private keys
        if ext in SENSITIVE_EXTENSIONS or basename in SENSITIVE_FILENAMES:
            return False

        # Reject excluded directories
        parts = path.replace("\\", "/").split("/")
        for part in parts:
            if part in DEFAULT_EXCLUDED_DIRS:
                return False

        return True

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        q = query.lower().strip()
        if len(q) < 2:
            return []

        # Sample curated files for instant indexing & verification
        sample_files = [
            ("file:cargo-toml", "Cargo.toml", "Root Rust workspace specification", "d:/My own os/Cargo.toml"),
            ("file:readme-md", "README.md", "NEXUS OS architectural overview and pillars", "d:/My own os/README.md"),
            ("file:design-system", "DESIGN_SYSTEM.md", "Aether design tokens, corner radii, themes", "d:/My own os/DESIGN_SYSTEM.md"),
            ("file:architecture", "ARCHITECTURE.md", "Systems engineering, IPC, and daemon specs", "d:/My own os/ARCHITECTURE.md"),
            ("file:spotlight-qml", "NexusSpotlightOverlay.qml", "Spotlight HUD Wayland overlay component", "d:/My own os/src/spotlight/qml/NexusSpotlightOverlay.qml")
        ]

        results = []
        for fid, title, desc, path in sample_files:
            if not self.is_safe_path(path):
                continue

            score = 0
            t_low = title.lower()
            if t_low == q:
                score = 900
            elif t_low.startswith(q):
                score = 700
            elif q in t_low or q in desc.lower():
                score = 450

            if score > 0:
                actions = [
                    {"id": "open", "title": "Open File", "shortcut": "Enter"},
                    {"id": "reveal", "title": "Reveal in Folder", "shortcut": "Ctrl+R"},
                    {"id": "copy_path", "title": "Copy Path", "shortcut": "Ctrl+C"}
                ]
                results.append(SearchResult(fid, title, desc, "Files", "📄", score,
                                            metadata={"path": path}, actions=actions))
        return results[:limit]


class AIModelProvider(SearchProvider):
    @property
    def category_name(self) -> str:
        return "AI Models"

    def __init__(self):
        self.models = [
            {"id": "model:qwen", "name": "qwen2.5-coder:7b", "role": "Code Intelligence", "status": "Loaded in VRAM (4.2GB)", "loaded": True},
            {"id": "model:llama", "name": "llama3.2:3b", "role": "Fast Reasoning", "status": "Available in Ollama (2.0GB)", "loaded": False},
            {"id": "model:deepseek", "name": "deepseek-r1:8b", "role": "Deep Math & Reasoning", "status": "Available (4.9GB)", "loaded": False},
            {"id": "model:nomic", "name": "nomic-embed-text", "role": "Semantic Vector Search", "status": "Active in VRAM (0.3GB)", "loaded": True}
        ]

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        q = query.lower().strip()
        results = []
        for m in self.models:
            name = m["name"].lower()
            role = m["role"].lower()
            score = 0
            if q in name or q in role or q in "ai model ollama":
                score = 750 if name.startswith(q) else 500

            if score > 0:
                actions = [
                    {"id": "toggle_load", "title": "Unload from VRAM" if m["loaded"] else "Load into VRAM", "shortcut": "Enter"},
                    {"id": "prompt", "title": "Spawn AI Chat Session", "shortcut": "Ctrl+P"}
                ]
                desc = f"{m['role']} • {m['status']}"
                results.append(SearchResult(m["id"], m["name"], desc, "AI Models", "🤖", score,
                                            metadata=m, actions=actions))
        return results[:limit]


class SystemActionsProvider(SearchProvider):
    @property
    def category_name(self) -> str:
        return "System Actions"

    def __init__(self):
        self.actions = [
            SearchResult("sys:lock", "Lock Workstation", "Lock display session and require password", "System Actions", "🔒",
                         actions=[{"id": "lock", "title": "Lock Now", "shortcut": "Enter", "destructive": False}]),
            SearchResult("sys:logout", "Log Out", "End current desktop session", "System Actions", "🚪",
                         actions=[{"id": "logout", "title": "Log Out", "shortcut": "Enter", "destructive": True, "warning": "Unsaved work in open applications will be lost."}]),
            SearchResult("sys:restart", "Restart System", "Reboot NEXUS OS workstation", "System Actions", "🔄",
                         actions=[{"id": "restart", "title": "Restart Workstation", "shortcut": "Enter", "destructive": True, "warning": "All background processes will terminate."}]),
            SearchResult("sys:shutdown", "Shut Down", "Power off hardware safely", "System Actions", "⏻",
                         actions=[{"id": "shutdown", "title": "Power Off", "shortcut": "Enter", "destructive": True, "warning": "System will power off immediately."}]),
            SearchResult("sys:theme_toggle", "Toggle Dark / Light Theme", "Switch between Obsidian dark and Paper light", "System Actions", "🌓",
                         actions=[{"id": "toggle_theme", "title": "Switch Theme", "shortcut": "Enter", "destructive": False}]),
            SearchResult("sys:wifi_toggle", "Toggle Wi-Fi", "Turn wireless networking on or off", "System Actions", "📶",
                         actions=[{"id": "toggle_wifi", "title": "Toggle Wi-Fi", "shortcut": "Enter", "destructive": False}]),
            SearchResult("sys:bluetooth_toggle", "Toggle Bluetooth", "Turn Bluetooth adapter on or off", "System Actions", "ᛒ",
                         actions=[{"id": "toggle_bluetooth", "title": "Toggle Bluetooth", "shortcut": "Enter", "destructive": False}])
        ]

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        q = query.lower().strip()
        results = []
        for act in self.actions:
            score = 0
            t_low = act.title.lower()
            if t_low == q:
                score = 900
            elif t_low.startswith(q):
                score = 750
            elif q in t_low or q in act.description.lower():
                score = 500

            if score > 0:
                act_copy = SearchResult(act.id, act.title, act.description, act.category,
                                        act.icon, score, act.metadata, act.actions)
                results.append(act_copy)
        return results[:limit]


class CommandProvider(SearchProvider):
    @property
    def category_name(self) -> str:
        return "Commands"

    def __init__(self):
        self.presets = [
            ("cmd:cargo_build", "cargo build", "Compile active workspace packages", "cargo build"),
            ("cmd:cargo_test", "cargo test", "Execute test harnesses across workspace", "cargo test"),
            ("cmd:podman_ps", "podman ps", "List running container environments", "podman ps"),
            ("cmd:ollama_ps", "ollama ps", "View models currently resident in VRAM", "ollama ps"),
            ("cmd:git_status", "git status", "Check branch status and uncommitted files", "git status"),
            ("cmd:git_pull", "git pull --rebase", "Fetch and rebase remote branch", "git pull --rebase")
        ]

    def is_destructive(self, cmd: str) -> bool:
        for pattern in DESTRUCTIVE_PATTERNS:
            if pattern.search(cmd):
                return True
        return False

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        q = query.strip()
        results = []

        # If user explicitly types a command prefixed with '>' or terminal commands
        for cid, title, desc, cmd_str in self.presets:
            score = 0
            if q.lower() in title.lower():
                score = 700 if title.startswith(q.lower()) else 450

            if score > 0:
                is_dest = self.is_destructive(cmd_str)
                actions = [{
                    "id": "run",
                    "title": "Execute Command",
                    "shortcut": "Enter",
                    "destructive": is_dest,
                    "warning": f"Command '{cmd_str}' may be destructive. Confirm execution?" if is_dest else ""
                }]
                results.append(SearchResult(cid, f"> {title}", desc, "Commands", "⚡", score,
                                            metadata={"command": cmd_str}, actions=actions))

        # Dynamic command execution if query starts with '>'
        if q.startswith(">") and len(q) > 1:
            raw_cmd = q[1:].strip()
            is_dest = self.is_destructive(raw_cmd)
            actions = [{
                "id": "run",
                "title": f"Execute '{raw_cmd}'",
                "shortcut": "Enter",
                "destructive": is_dest,
                "warning": f"Executing arbitrary command '{raw_cmd}'. Confirm execution?" if is_dest else ""
            }]
            results.insert(0, SearchResult("cmd:custom", f"> {raw_cmd}", "Run CLI command in user shell", "Commands", "⚡",
                                          score=950, metadata={"command": raw_cmd}, actions=actions))

        return results[:limit]


class WebSearchProvider(SearchProvider):
    @property
    def category_name(self) -> str:
        return "Web Search"

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        q = query.strip()
        if not q or len(q) < 2:
            return []

        actions = [
            {"id": "web_ddg", "title": "Search DuckDuckGo", "shortcut": "Enter"},
            {"id": "web_google", "title": "Search Google", "shortcut": "Ctrl+G"}
        ]
        return [SearchResult(
            "web:query",
            f"Search web for '{q}'",
            "Open query in default developer web browser",
            "Web Search",
            "🌐",
            score=150,
            metadata={"query": q},
            actions=actions
        )]


# -----------------------------------------------------------------------------
# Master Spotlight Search Engine
# -----------------------------------------------------------------------------
class SpotlightEngine:
    def __init__(self, db_path: Optional[str] = None):
        self.db = SearchDatabase(db_path)
        self.providers: List[SearchProvider] = [
            ApplicationProvider(),
            ProjectProvider(),
            FileProvider(),
            AIModelProvider(),
            SystemActionsProvider(),
            CommandProvider(),
            WebSearchProvider()
        ]

    def register_provider(self, provider: SearchProvider):
        self.providers.append(provider)

    def search(self, query: str, category_filter: Optional[str] = None, limit: int = 12) -> List[Dict[str, Any]]:
        clean_q = query.strip()
        if not clean_q:
            # Return recent items or top applications when query is empty
            return self._get_default_launcher_items()

        results: List[SearchResult] = []
        for provider in self.providers:
            if category_filter and category_filter != "All" and provider.category_name != category_filter:
                continue
            try:
                provider_results = provider.search(clean_q, limit=limit)
                results.extend(provider_results)
            except Exception as e:
                print(f"Error querying provider {provider.category_name}: {e}", file=sys.stderr)

        # Apply usage frequency and recency boost from SQLite DB
        with self.db._get_connection() as conn:
            for item in results:
                row = conn.execute(
                    "SELECT launch_count, last_launched FROM usage_history WHERE item_id = ?",
                    (item.id,)
                ).fetchone()
                if row:
                    launch_count, last_launched = row[0], row[1]
                    # Frequency boost up to 200 pts
                    item.score += min(launch_count * 25, 200)
                    # Recency boost (within 24 hours): +50 pts
                    if time.time() - last_launched < 86400:
                        item.score += 50

        # Sort by relevance score descending
        results.sort(key=lambda x: x.score, reverse=True)
        return [res.to_dict() for res in results[:limit]]

    def _get_default_launcher_items(self) -> List[Dict[str, Any]]:
        app_prov = ApplicationProvider()
        defaults = app_prov.apps[:5]
        return [item.to_dict() for item in defaults]

    def record_launch(self, item_id: str):
        self.db.record_usage(item_id)

    def check_shortcut_conflict(self, shortcut: str = "Meta+Space") -> Dict[str, Any]:
        """
        Detects if Windows/Super+Space conflicts with existing Linux IBus or desktop shortcuts.
        """
        # In Linux environments, checks /desktop/ibus/general/hotkey/triggers via gsettings or env
        is_linux = sys.platform.startswith("linux")
        conflict_detected = False
        conflict_source = ""

        if is_linux:
            ibus_hotkey = os.popen("gsettings get org.freedesktop.ibus.general.hotkey triggers 2>/dev/null").read().strip()
            if "space" in ibus_hotkey.lower() and ("super" in ibus_hotkey.lower() or "win" in ibus_hotkey.lower()):
                conflict_detected = True
                conflict_source = "IBus Input Method Switcher"

        return {
            "shortcut": shortcut,
            "has_conflict": conflict_detected,
            "conflict_source": conflict_source,
            "recommended_alternatives": ["Alt+Space", "Ctrl+Space", "Meta+Shift+Space"]
        }


# Global engine instance
_engine_instance: Optional[SpotlightEngine] = None

def get_engine() -> SpotlightEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = SpotlightEngine()
    return _engine_instance
