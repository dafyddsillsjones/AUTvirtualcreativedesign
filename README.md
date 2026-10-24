# VCDRC Project Lab

A focused, single-purpose research idea explorer, designed to visually harmonise with the VCDRC website.

## Publish
Upload `index.html`, `data.json` and `publications.json` to the root of your GitHub Pages repository, replacing the previous files.

## Evidence and limitations
The existing 36-member directory and centre-project associations remain in `data.json`, but no longer appear as directories in the interface. `publications.json` is currently empty: no full AUT publication import has been completed. The tool matches words against indexed titles/tags and publication text; it does not yet provide semantic AI reasoning. Members are treated as available as requested. The design is an interpretation of VCDRC's publicly visible university style, not an exact licensed reproduction.

To enrich publications, populate `publications.json` with objects like:
`{"title":"...", "authors":["Exact Member Name"],"year":2025,"url":"https://...", "abstract":"...", "subjects":["..."],"methods":["..."]}`
Only use methods/subjects grounded in the output. The UI will incorporate these automatically.
