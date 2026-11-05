# Publication state

Checked 5 November 2026.

- Repository: https://github.com/martaforjaz/metagenomic-binning-benchmark-atlas . Public GitHub HTML returned HTTP 200 and a Public visibility marker; the prepared resource was pushed to main successfully. The initial commit was preserved.
- The complete static site is in `site/`. Its publication branch `gh-pages` was pushed and verified by a read-only remote-reference check, using a Git commit built from that directory; no administrative attachments or third-party video/illustration are present.
- Expected Pages URL: https://martaforjaz.github.io/metagenomic-binning-benchmark-atlas/ . **Live deployment is not confirmed.** The active proxy denies this domain, and GitHub API calls return Forbidden, preventing automatic Pages configuration/status checks. This is an access limitation, not proof that Pages is absent or broken.
- To activate the prepared branch if Pages is not already enabled: open repository **Settings → Pages → Build and deployment → Deploy from a branch → gh-pages → / (root) → Save**. Native Git authentication already works; no new personal token is requested.
- The repository workflow runs scientific reproduction and the official example on GitHub Actions. Local checks passed; a remote Actions success is not claimed without inspection.

Environment configuration draft: dependency installation/reproduction instructions and startup guidance were saved, together with the additional primary-source/API/Pages domain requirements. Review and save these settings, then publish the environment to activate its draft. This is separate from publishing this Git repository or enabling GitHub Pages.

For subsequent updates, commit the regenerated site and run `bash scripts/publish_site.sh`. The script verifies nonempty Git objects, preserves the existing Pages parent and uses a normal fast-forward push. It does not enable Pages settings.
