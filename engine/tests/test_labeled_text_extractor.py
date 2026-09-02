"""labeled_text extractor (Codex post-merge findings c/h on PR18): a prose answer must not flow
whole into a single-value slot. Exactly one "<label>: <text>" line is taken verbatim; a missing
or duplicated label REJECTS BY NAME (fail-closed), mirroring labeled_integer."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import setup  # noqa: E402,F401
sys.path.insert(0, str(ROOT / "engine"))
import placeholders  # noqa: E402

ANSWER = ("The agreement is sent and signed through InkPath, and the W-9 goes out attached.\n"
          "E-signature tool: InkPath\n"
          "Company signer: Sloane Karr, Principal Broker\n"
          "CROSS-SEAT: InkPath is the same e-signature tool the leasing seat uses.\n")


class LabeledText(unittest.TestCase):
    def test_takes_exactly_the_labeled_line_verbatim(self):
        print("ARMED: a labeled_text row yields the labeled line only, never the surrounding prose")
        row = {"extractor": "labeled_text", "label": "E-signature tool"}
        self.assertEqual(placeholders.extract_value(row, ANSWER, {}), "InkPath")
        row = {"extractor": "labeled_text", "label": "Company signer"}
        self.assertEqual(placeholders.extract_value(row, ANSWER, {}), "Sloane Karr, Principal Broker")

    def test_missing_label_rejects_by_name(self):
        print("ARMED: a missing labeled line rejects naming the label")
        with self.assertRaisesRegex(ValueError, "labeled text line 'Turnaround': not found"):
            placeholders.extract_value({"extractor": "labeled_text", "label": "Turnaround"}, ANSWER, {})

    def test_duplicated_label_rejects_by_name(self):
        with self.assertRaisesRegex(ValueError, "appears more than once"):
            placeholders.extract_value({"extractor": "labeled_text", "label": "E-signature tool"}, ANSWER + "E-signature tool: Other\n", {})

    def test_registered_as_a_supported_extractor(self):
        self.assertIn("labeled_text", placeholders.SUPPORTED_EXTRACTORS)


if __name__ == "__main__":
    unittest.main()
