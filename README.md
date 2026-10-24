# VCDRC Project Lab — public research importer

The interface is single-purpose: enter a research idea, see up to three evidence-linked collaborators, and progressively explore related work. Existing VCDRC projects are already indexed. Public academic works will populate `publications.json` after the importer runs.

## Publish
Upload the entire directory contents (including `.github/workflows/research-update.yml` and `scripts/update_publications.py`) to the root of the GitHub repository. In **Actions → Update public research records → Run workflow**, start the import. The workflow runs monthly afterward and commits data back to the repository. Allow GitHub Actions read/write repository permissions under Settings → Actions → General → Workflow permissions if necessary.

## Identity and completeness
The importer searches all 36 member names, accepts only a single exact-name OpenAlex author record with AUT affiliation, retrieves up to 500 works per resolved author, and deduplicates by DOI/OpenAlex ID. Other authors are marked unresolved rather than misattributed. This is not guaranteed to retrieve all publications, AUT-only outputs, or practice research. `coverage.json` reports the gaps. No methods are fabricated from titles; subjects use OpenAlex indexed topics. Manual ORCID resolution and additional Tuwhera/AUT profile sources are needed for full coverage.

## Caution
This tool is a transparent lexical recommender, not a semantic AI model. Project and publication matches should be reviewed before using them in funding decisions. The cropped header is sourced from a screenshot provided for design reference; replace with an original licensed site image for production.
