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
import tempfile
import time
import unittest
from threading import Thread
from follower import Follower


log_example = """2021-07-13T12:03:07.902859782Z stdout F Lorem ipsum dolor sit amet, consectetur adipiscing elit.
2021-07-13T12:03:07.903195293Z stdout F In in ante nec diam pellentesque consectetur in sit amet leo.
2021-07-13T12:03:07.90370176Z stdout F Vivamus eu sapien at ipsum suscipit rhoncus.
2021-07-13T12:03:09.83225183Z stdout F Etiam sed enim facilisis, aliquet elit et, hendrerit metus.
2021-07-13T12:03:09.832302935Z stdout F Cras eget imperdiet lacus, id auctor neque.
"""


class TestFollower(unittest.TestCase):
    def setUp(self):
        self.test_filename = tempfile.mktemp()
        os.mknod(self.test_filename)

    def test_follows_file(self):
        writer_thread = Thread(
            target=write_to_file_and_delete, args=(2, self.test_filename)
        )
        writer_thread.start()

        result = ""
        with Follower(self.test_filename) as f:
            for line in f.lines():
                result += line + "\n"

        self.assertEqual(log_example, result)


def write_to_file_and_delete(self, test_filename):
    with open(test_filename, "w") as file:
        for line in log_example.split("\n"):
            file.write(line + "\n")
            file.flush()
            time.sleep(1)
    os.remove(file.name)


if __name__ == "__main__":
    unittest.main()
