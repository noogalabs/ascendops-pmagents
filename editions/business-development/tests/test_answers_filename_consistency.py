"""(a) Codex post-merge P1 on PR18: the engine writes the mapping's declared structured answers
filename (business-development-config.json) while AGENTS.md and ONBOARDING.md told the agent to read
seat-config.json, so first boot opened a file that does not exist. Every runtime reference to the
answers file in the shipped library must equal the declared filename, by file and line."""
import json, re, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "engine"))
import cross_seat  # noqa: E402
LIBRARY = ROOT / "editions" / "business-development" / "library-src"
MAPPING = json.loads((ROOT / "engine" / "mappings" / "business-development.json").read_text())
ANSWERS_FILE_RE = re.compile(r"`?([a-z-]+-config\.json|seat-config\.json)`?")


class AnswersFilenameConsistency(unittest.TestCase):
    def test_every_runtime_reference_names_the_declared_answers_file(self):
        print("ARMED: a runtime doc naming any other answers filename than the mapping declares fails here by file:line")
        declared = cross_seat.structured_answers_filename(MAPPING)
        self.assertEqual(declared, "business-development-config.json")
        wrong = []
        for doc in sorted(LIBRARY.rglob("*.md")):
            for n, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
                for m in ANSWERS_FILE_RE.finditer(line):
                    if m.group(1) != declared and "seat_config_schema" not in line:
                        wrong.append(f"{doc.relative_to(ROOT)}:{n}: {m.group(1)}")
        self.assertEqual(wrong, [], "runtime references to a non-declared answers filename")

    def test_the_declared_answers_file_is_referenced_by_first_boot(self):
        agents = (LIBRARY / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("business-development-config.json", agents, "first boot must name the declared answers file")


if __name__ == "__main__":
    unittest.main()
