import csv
from pathlib import Path
from shutil import copytree
from tempfile import TemporaryDirectory
import unittest

from inspect_inputs import DEFAULT_INPUT, inspect_inputs


class InputPackTests(unittest.TestCase):
    def test_bundled_inputs_are_resolvable(self):
        result = inspect_inputs(DEFAULT_INPUT)
        self.assertTrue(result["input_pack"])
        self.assertTrue(result["tables"])
        self.assertTrue(all(result["tables"].values()))

    def test_altered_delivery_is_detected(self):
        with TemporaryDirectory() as scratch:
            cloned = Path(scratch) / "data"
            copytree(DEFAULT_INPUT, cloned)
            path = sorted(cloned.glob("*.csv"))[0]
            with path.open("a", encoding="utf-8", newline="") as stream:
                csv.writer(stream).writerow(["altered"])
            with self.assertRaisesRegex(ValueError, "digest differs"):
                inspect_inputs(cloned)
