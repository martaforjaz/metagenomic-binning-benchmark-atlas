#!/usr/bin/env bash
# Publish committed static content without requiring git-subtree or rewriting history.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git diff --quiet -- site
git diff --cached --quiet -- site
atlas_site_tree=$(git rev-parse --verify HEAD:site)
test -n "$atlas_site_tree"
atlas_parent_args=()
atlas_remote_ref=$(git ls-remote --heads origin gh-pages)
if test -n "$atlas_remote_ref"; then
    git fetch origin gh-pages
    atlas_parent=$(git rev-parse --verify FETCH_HEAD)
    test -n "$atlas_parent"
    atlas_parent_args=(-p "$atlas_parent")
fi
atlas_pages_commit=$(git -c user.name='Marta Forjaz' -c user.email='martaforjaz@users.noreply.github.com' commit-tree "$atlas_site_tree" "${atlas_parent_args[@]}" -m 'Publish validated static benchmark atlas')
test -n "$atlas_pages_commit"
git push origin "$atlas_pages_commit:refs/heads/gh-pages"
