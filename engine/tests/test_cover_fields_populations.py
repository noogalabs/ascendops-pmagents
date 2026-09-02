"""Cover-field POPULATIONS guard (task_1788292812277).

Three places declare cover fields: intake.COVER_FIELDS (the base), each edition
mapping's optional `cover_fields` list (leasing and turnover declare their own,
which REPLACES the base), and engine.cover_fields_for_mapping's set-default merge
(the engine-consumed autonomy fields). A field added to the base alone does not
reach mapping-declared seats, and PR34's zero-touch suite caught exactly that.
This guard makes the trap fail BY NAME: every seat must resolve every base field,
and the engine's merge list must itself be a subset of the base.
"""
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("glue_engine_cover_fields", HERE / "engine.py")
engine = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(engine)
intake = engine.intake


class CoverFieldPopulations(unittest.TestCase):
    def test_every_seat_resolves_every_base_cover_field_by_name(self):
        print("ARMED: a base cover field that a mapping-declared seat cannot parse must fail here by seat and label")
        base = dict(intake.COVER_FIELDS)
        missing = {}
        for seat in sorted(engine.SUPPORTED):
            resolved = engine.cover_fields_for_seat(seat)
            gaps = {label: key for label, key in base.items() if resolved.get(label) != key}
            if gaps:
                missing[seat] = gaps
        self.assertEqual(missing, {}, f"seats missing base cover fields (label -> key): {missing}")

    def test_engine_merge_list_is_a_subset_of_the_base(self):
        print("ARMED: the engine's set-default merge must not carry a field the base does not declare")
        merged = engine.cover_fields_for_mapping({"cover_fields": [{"label": "Company name", "key": "company_name"}]})
        extra = {label: key for label, key in merged.items()
                 if label != "Company name" and intake.COVER_FIELDS.get(label) != key}
        self.assertEqual(extra, {}, f"engine merge carries fields absent from intake.COVER_FIELDS: {extra}")

    def test_planted_base_field_without_engine_merge_fails_on_mapping_declared_seats(self):
        """THE TRAP, driven: add a base field and touch nothing else. Mapping-declared seats
        (leasing, turnover) must be reported by name; base-inheriting seats must not."""
        print("ARMED: planted base field must surface leasing + turnover by name, not the inheriting seats")
        planted = dict(intake.COVER_FIELDS, **{"Planted field": "planted_field"})
        original = intake.COVER_FIELDS
        try:
            intake.COVER_FIELDS = planted
            failing = sorted(seat for seat in engine.SUPPORTED
                             if engine.cover_fields_for_seat(seat).get("Planted field") != "planted_field")
        finally:
            intake.COVER_FIELDS = original
        declared = sorted(seat for seat in engine.SUPPORTED
                          if engine.load_seat_mapping(seat).get("cover_fields") is not None)
        self.assertEqual(failing, declared, "the trap must bite exactly the mapping-declared seats")
        self.assertTrue(declared, "guard subject lost: no seat declares its own cover_fields any more")


if __name__ == "__main__":
    unittest.main()
