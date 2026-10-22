# KubeClipper documentation

Bilingual documentation for [KubeClipper](https://github.com/kubeclipper/kubeclipper), built with Hugo and Docsy.

## Prerequisites

- Hugo **extended 0.101.0** (the version used in CI)
- Node.js 24 and npm
- Python 3.12
- Git and Go (for Hugo modules)

```bash
npm ci
python3 -m pip install -r requirements.txt
```

Use a Python virtual environment if required by your operating system.

## Preview current documentation

```bash
make server
```

Open <http://localhost:1313>. This builds the current working content and serves the generated files; rebuild after editing. The preview does not include archived versions.

## Build and check every version

```bash
make check
```

The current working content is published at `/` and `/v1.7/`, with English at `/en/` and `/v1.7/en/`. Version 1.6 is built from the explicit bilingual sources in `versions/1.6/content`, based on the v1.6.0 release tag; the documentation repository has no `release/1.6` branch. Versions 1.5 through 1.1 are read from the canonical repository's `release/*` branches.

The builder fetches archives into `refs/remotes/docs-history/release/*`. It does not switch branches or merge into your checkout. Archived content and static assets use the current build tooling. To reuse already fetched refs without network access:

```bash
python3 scripts/build.py --host=https://kubeclipper.io --multi-versions --no-out-fetch
python3 scripts/check-site.py public
```

Missing historical refs fail the build. `public/` and `_output/` are generated directories. The checker validates local links and assets in regular current, 1.7, and bundled 1.6 pages, checks section anchors in current and 1.7 pages, and verifies all historical language entry points. Docsy print views are excluded because the theme's community text contains links relative to the original page. Historical content is preserved rather than silently rewritten.

## CI and publication

Pull requests build and validate the whole site and upload a `documentation-site` artifact. Only successful builds on the canonical repository's `master` publish to `gh-pages`. Fork builds produce artifacts without deploying the public site.

Update `CURRENT_VERSION` and `VERSION_ARRAY` in `scripts/builder/consts.py` when preparing a new documentation release. Before changing the current version again, preserve 1.7 content and assets in `release/1.7` and add it to the archive list. A local build or a Git commit does not establish that GitHub Pages has deployed.
