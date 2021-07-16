# Copyright 2021 kloeckner.i GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from queue import Queue
from watchdog.observers import Observer
from watchdog.events import (
    EVENT_TYPE_DELETED,
    EVENT_TYPE_MODIFIED,
    FileSystemEventHandler,
)


class Follower:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, "r")

        self.fs_events = Queue()
        self.fs_event_observer = Observer()
        self.fs_event_observer.schedule(QueuedEventHandler(self), filename)

    def __enter__(self):
        self.fs_event_observer.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.fs_event_observer.stop()
        self.file.close()

    def lines(self):
        # Read all existing lines
        while True:
            line = self.file.readline()
            if not line:
                break

            yield line.rstrip("\n")

        # Wait for new lines
        self.fs_events.empty()
        while True:
            event = self.fs_events.get()
            if event.event_type == EVENT_TYPE_DELETED:
                break
            elif event.event_type == EVENT_TYPE_MODIFIED:
                line = self.file.readline().rstrip("\n")
                if not line:
                    # On some platforms watchdog mistakenly sends a modified event on deletions.
                    if not os.path.exists(self.filename):
                        break

                    continue

                yield line


class QueuedEventHandler(FileSystemEventHandler):
    def __init__(self, parent):
        self._parent = parent

    def on_any_event(self, event):
        if not event.is_directory:
            self._parent.fs_events.put(event)
