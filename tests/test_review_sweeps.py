from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
MAPPINGS = ENGINE / "mappings"
LEDGER = ENGINE / "edition-review-ledger.json"
STANDARD_COVER = {"company_name", "org_short_name", "forward_email", "timezone"}
PROMISE_WORDS = re.compile(
    r"\b(must|blocker|never|each|every|graduate|autonomous|automatically)\b", re.I
)
QUESTION = re.compile(r"^([A-D]\d+)\.")


def load_ledger():
    return json.loads(LEDGER.read_text())


class ReviewSweepTests(unittest.TestCase):
    def test_named_ordering_rejects_prose_and_preserves_numeric_comparison(self):
        print("ARMED: ordering rejects prose and preserves numeric comparisons")
        import sys
        sys.path.insert(0, str(ENGINE))
        import cross_seat
        with self.assertRaisesRegex(TypeError, "is not numeric"):
            cross_seat._ordering_passes("2 delivery methods", "60 days", "gte")
        self.assertTrue(cross_seat._ordering_passes("60", 30, "gte"))
        self.assertFalse(cross_seat._ordering_passes("10", 30, "gte"))

    def test_named_declared_configuration_has_a_runtime_consumer(self):
        print("ARMED: every declared edition value has a non-setup consumer")
        ledger = load_ledger()
        for seat, row in ledger["editions"].items():
            if not row["mapping_driven"]:
                continue
            mapping = json.loads((MAPPINGS / row["mapping"]).read_text())
            library = ROOT / "editions" / row["edition"] / "library-src"
            runtime = "\n".join(
                path.read_text(errors="ignore")
                for path in library.rglob("*")
                if path.is_file() and path.name not in {"ONBOARDING.md", "README.md"}
            )
            placeholder_sources = {item["source"] for item in mapping.get("placeholders", [])}
            config_sources = {
                item["source"] for item in mapping.get("config_keys", [])
                if item.get("value_from") != "pointer"
            }
            for cover in mapping.get("cover_fields", []):
                if cover["key"] in STANDARD_COVER:
                    continue
                source = f"cover.{cover['key']}"
                self.assertIn(source, placeholder_sources | config_sources,
                              f"{seat} unconsumed cover field {source}")
            for item in mapping.get("placeholders", []):
                if item.get("extractor") == "literal":
                    continue
                token = "{{" + item["placeholder"] + "}}"
                config_landing = f'"{item["placeholder"]}"' in runtime
                self.assertTrue(token in runtime or config_landing,
                                f"{seat} placeholder has no runtime carrier or config landing: {token}")

    def test_named_companion_claims_equal_shipped_files(self):
        print("ARMED: companion claims equal the shipped edition files")
        for seat, row in load_ledger()["editions"].items():
            library = ROOT / "editions" / row["edition"] / "library-src"
            shipped = {path.name for path in library.iterdir() if path.is_file()}
            for name in row["companions"]:
                self.assertIn(name, shipped, f"{seat} claims missing companion {name}")
            edition = ROOT / "editions" / row["edition"]
            fixtures = list((edition / "fixtures").glob("ridgeline-*-answers.md"))
            self.assertEqual(len(fixtures), 1, f"{seat} must ship exactly one ridgeline fixture")
            for carrier in [edition / "answers-format.md", fixtures[0]]:
                text = carrier.read_text()
                self.assertIn(row["companion_claim"], text,
                              f"{seat} companion truth absent from {carrier.name}")
                for stale in row.get("banned_companion_claims", []):
                    self.assertNotIn(stale, text,
                                     f"{seat} retains false companion claim {stale} in {carrier.name}")

    def test_named_every_edition_onboarding_bash_block_parses(self):
        print("ARMED: every edition onboarding Bash fence passes bash -n")
        for seat, row in load_ledger()["editions"].items():
            onboarding = ROOT / "editions" / row["edition"] / "library-src" / "ONBOARDING.md"
            if not onboarding.exists():
                continue
            blocks = re.findall(r"(?m)^([ \t]*)```bash\n(.*?)\n\1```$",
                                onboarding.read_text(), re.S)
            self.assertGreater(len(blocks), 0, f"{seat} has no Bash fence census")
            for index, (_, block) in enumerate(blocks, 1):
                parsed = subprocess.run(["bash", "-n"], input=block, text=True,
                                        capture_output=True, check=False)
                self.assertEqual(parsed.returncode, 0,
                                 f"{seat} Bash block {index}: {parsed.stderr}")

    def test_named_questionnaire_promises_are_ledgered(self):
        print("ARMED: every questionnaire promise candidate has a review disposition")
        ledger = load_ledger()
        self.assertEqual(ledger["promise_wordlist"],
                         ["must", "blocker", "never", "each", "every",
                          "graduate", "autonomous", "automatically"])
        for seat, row in ledger["editions"].items():
            questionnaire = ROOT / "editions" / row["edition"] / "answers-format.md"
            current = "INTRO"
            candidates = set()
            for line in questionnaire.read_text().splitlines():
                match = QUESTION.match(line)
                if match:
                    current = match.group(1)
                if PROMISE_WORDS.search(line):
                    candidates.add(current)
            dispositions = row["promise_ledger"]
            self.assertEqual(candidates, set(dispositions),
                             f"{seat} promise ledger is incomplete")
            for subject, disposition in dispositions.items():
                valid = (
                    {"gate_surface", "named_test"} <= set(disposition)
                    or "no_gate_reason" in disposition
                    or "successor_task" in disposition
                )
                self.assertTrue(valid, f"{seat} {subject} has no reviewable disposition")


if __name__ == "__main__":
    unittest.main()
