import threading
import time
from pathlib import Path

from projtree.watcher import watch_and_generate


def test_watcher_regenerates_on_new_file(tmp_path: Path):
    output = tmp_path / "STRUCTURE.md"

    watcher_thread = threading.Thread(
        target=watch_and_generate,
        kwargs={
            "root_path": tmp_path,
            "output_path": output,
            "debounce_seconds": 0.1,
        },
        daemon=True,
    )
    watcher_thread.start()

    time.sleep(0.2)

    # Trigger structural change
    (tmp_path / "new_file.txt").write_text("hello")

    time.sleep(0.4)

    assert output.exists()
    contents = output.read_text(encoding="utf-8")

    assert "new_file.txt" in contents
