# Custom structured-artifact rerun fix

Base: merged PM-assist main `98706ca0`.

## Defect

The mapping engine translated the canonical `seat-config.json` output to a
mapping-declared filename after every run, but did not recreate the canonical
counterpart before a managed rerun. The first mapping seat with a custom
declared filename therefore configured once and rejected its second production
`configure()` call before materialization.

## Fix

At the engine boundary, after the existing managed-rerun/version acceptance and
before the mapping core runs, a custom declared artifact is copied byte-for-byte
to the absent canonical counterpart. The trigger requires a custom filename, an
accepted managed manifest, a present declared artifact, and an absent canonical
artifact. The declared artifact stays in place for the existing post-run
stale-counterpart disposal. A present-but-different counterpart rejects, and the
declared payload must name the seat being configured. The sealed core is
unchanged.

## Armed validation

- The registry-parameterized production casualty configures every mapping seat
  twice using its own conventional fixture and mapping-declared filename. It
  contains explicit non-vacuity guards for both custom and default filenames.
- Disabling pre-run recreation kills the custom consumer on call two.
- Weakening the genuine-conflict rejection kills its named casualty.
- Weakening the seat-identity check kills the cross-seat-counterfeit casualty.
- The default-filename PM-assist path remains green inside the registry loop.

The focused engine suite passes 15/15 after all three mutations are restored.
