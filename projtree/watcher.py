from __future__ import annotations

import logging
import threading
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .generator import generate_markdown_tree
from .ignore import is_ignored, DEFAULT_IGNORES, load_ignore_file

logger = logging.getLogger(__name__)


def _build_ignore_set(
    root_path: Path,
    extra_ignores: set[str] | None = None,
) -> set[str]:
    ignore: set[str] = set()
    ignore |= DEFAULT_IGNORES
    ignore |= load_ignore_file(root_path)
    ignore |= set(extra_ignores or set())
    return ignore


class _DebouncedHandler(FileSystemEventHandler):
    def __init__(
        self,
        root_path: Path,
        output_path: Path,
        debounce_seconds: float,
        extra_ignores: set[str] | None = None,
    ) -> None:
        self.root_path = root_path
        self.output_path = output_path
        self.debounce_seconds = debounce_seconds

        self._extra_ignores = set(extra_ignores or set())
        self._preloaded_ignores = load_ignore_file(root_path)

        self._lock = threading.Lock()
        self._timer: threading.Timer | None = None


    def on_any_event(self, event) -> None:
        path = Path(event.src_path)

        # Always react to .projtreeignore changes
        if path.name == ".projtreeignore":
            self._preloaded_ignores = load_ignore_file(self.root_path)
            self._schedule_regeneration()
            return

        # Ignore non-structural events
        if event.event_type == "modified":
            return

        # Unified ignore logic (includes output file)
        if is_ignored(
            path,
            self.root_path,
            extra_ignores=self._extra_ignores,
            preloaded_ignores=self._preloaded_ignores,
        ):
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
        ignore = _build_ignore_set(self.root_path, self._extra_ignores)

        markdown = generate_markdown_tree(self.root_path, ignore=ignore)

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
    initial_generate: bool = True,
    extra_ignores: set[str] | None = None,
) -> None:
    combined_extra_ignores = set(extra_ignores or set())
    try:
        output_path.resolve().relative_to(root_path.resolve())
        combined_extra_ignores.add(output_path.name)
    except ValueError:
        pass

    if initial_generate:
        ignore = _build_ignore_set(root_path, combined_extra_ignores)
        
        markdown = generate_markdown_tree(root_path, ignore=ignore)
        output_path.write_text(markdown, encoding="utf-8")

    while True:
        handler = _DebouncedHandler(
            root_path=root_path,
            output_path=output_path,
            debounce_seconds=debounce_seconds,
            extra_ignores=combined_extra_ignores,
        )

        observer = Observer()
        observer.schedule(handler, str(root_path), recursive=True)

        try:
            observer.start()
            while observer.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
            break
        except Exception as exc:
            observer.stop()
            observer.join()
            logger.exception("Watcher error, restarting after backoff: %s", exc)
            time.sleep(1.0)  # restart backoff
            continue
