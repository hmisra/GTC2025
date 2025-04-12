#!/bin/bash

# This script will create a new branch with the fixed commit messages
# This avoids the need for interactive rebase

# Create a new branch from a point before our commits
git checkout -b fixed-commits 8355de95e6c3680b1dc58752bc0045c78d41a732~1

# Cherry-pick the first commit with a new message
git cherry-pick -n 8355de95e6c3680b1dc58752bc0045c78d41a732
git commit --amend -m "Refactor project structure and enhance GTC 2025 analysis"

# Cherry-pick the second commit with a new message
git cherry-pick -n d8d4e61817d50b9075c8a5f4f43c96a0141be249
git commit --amend -m "Remove temporary commit message file"

echo "New branch 'fixed-commits' created with clean commit messages."
echo "To apply these changes to main:"
echo "  git checkout main"
echo "  git reset --hard fixed-commits"
echo "  git push --force-with-lease origin main" 