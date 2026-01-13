from __future__ import annotations

import threading
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .generator import generate_markdown_tree
from .ignore import is_ignored


class _DebouncedHandler(FileSystemEventHandler):
    def __init__(
        self,
        root_path: Path,
        output_path: Path,
        debounce_seconds: float,
    ) -> None:
        self.root_path = root_path
        self.output_path = output_path
        self.debounce_seconds = debounce_seconds

        self._lock = threading.Lock()
        self._timer: threading.Timer | None = None

    def on_any_event(self, event) -> None:
        path = Path(event.src_path)

        # Ignore output file to prevent loops
        if path.resolve() == self.output_path.resolve():
            return

        # Ignore non-structural events
        if event.event_type == "modified":
            return

        # Apply project ignore rules
        if is_ignored(path, self.root_path):
            return

        self._schedule_regeneration()

    def _schedule_regeneration(self) -> None:
        with self._lock:
            if self._timer:
                self._timer.cancel()

            self._timer = threading.Timer(
                self.debounce_seconds,
                self._regenerate,
            )
            self._timer.daemon = True
            self._timer.start()

    def _regenerate(self) -> None:
        markdown = generate_markdown_tree(self.root_path)

        if self.output_path.exists():
            existing = self.output_path.read_text(encoding="utf-8")
            if existing == markdown:
                return

        self.output_path.write_text(markdown, encoding="utf-8")


def watch_and_generate(
    root_path: Path,
    output_path: Path,
    *,
    debounce_seconds: float = 0.4,
) -> None:
    # INITIAL GENERATION (critical)
    markdown = generate_markdown_tree(root_path)
    output_path.write_text(markdown, encoding="utf-8")

    handler = _DebouncedHandler(
        root_path=root_path,
        output_path=output_path,
        debounce_seconds=debounce_seconds,
    )

    observer = Observer()
    observer.schedule(handler, str(root_path), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.join()
