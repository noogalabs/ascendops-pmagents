"""The business-development seat's messaging choice is LOAD-BEARING (piper PR18 seat LOW said the
"Resident messaging autonomy" line looked inapplicable and inert for BD; flipping it left the
suites green because no test consumed it). It gates every EXTERNAL_SEND category, which for BD is
the six prospect/owner-facing sends. Driven through the production entry (render + record-decision
CLI) on a copy of the BD library: choice NO keeps cold outreach locked at a met bar; choice YES
unlocks it; an internal BD category unlocks under either choice (control)."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import setup  # noqa: E402,F401
sys.path.insert(0, str(ROOT / "engine"))
import autonomy  # noqa: E402

BD_LIBRARY = ROOT / "editions" / "business-development" / "library-src"


class BusinessDevelopmentMessagingChoice(unittest.TestCase):
    def _seat(self, choice: str):
        tmp = Path(tempfile.mkdtemp(prefix="bd-choice-"))
        self.addCleanup(shutil.rmtree, tmp)
        root = tmp / "seat"
        shutil.copytree(BD_LIBRARY, root)
        settings = autonomy.parse_settings({"autonomy_mode": "copilot", "unlock_window": "last_3",
                                            "qualifying_accuracy": "90",
                                            "external_send_autonomy": choice})
        autonomy.render(root, settings, "2026-09-02T12:00:00Z")
        autonomy.write_engine_sidecar(root)
        return root

    def _record(self, root, category, n=3):
        for _ in range(n):
            r = subprocess.run([sys.executable, str(ROOT / "engine" / "engine.py"), "record-decision",
                                str(root), category, "--correct"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        return json.loads((root / "copilot-thresholds.json").read_text())["categories"][category]["status"]

    def test_choice_no_keeps_cold_outreach_locked_at_a_met_bar(self):
        print("ARMED: BD cold_outreach_first_touch at a met accuracy bar stays LOCKED when the messaging choice is no")
        self.assertEqual(self._record(self._seat("no"), "cold_outreach_first_touch"), "locked")

    def test_choice_yes_unlocks_cold_outreach_at_a_met_bar(self):
        print("ARMED: the same bar UNLOCKS cold_outreach_first_touch when the messaging choice is yes")
        self.assertEqual(self._record(self._seat("yes"), "cold_outreach_first_touch"), "unlocked")

    def test_internal_bd_category_unlocks_under_either_choice(self):
        print("CONTROL: alert_triage_note (internal) unlocks at the bar regardless of the messaging choice")
        self.assertEqual(self._record(self._seat("no"), "alert_triage_note"), "unlocked")
        self.assertEqual(self._record(self._seat("yes"), "alert_triage_note"), "unlocked")


if __name__ == "__main__":
    unittest.main()
