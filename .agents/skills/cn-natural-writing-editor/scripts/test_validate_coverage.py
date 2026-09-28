#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_coverage import validate  # noqa: E402


class CoverageContractTests(unittest.TestCase):
    def test_current_skill_satisfies_coverage_contract(self) -> None:
        skill_dir = Path(__file__).resolve().parents[1]
        result = validate(skill_dir)
        self.assertEqual(result["status"], "PASS", result["errors"])
        self.assertGreaterEqual(result["rows"], 10)


if __name__ == "__main__":
    unittest.main()
