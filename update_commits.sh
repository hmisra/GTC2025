#!/bin/bash

# Amend the most recent commit without [Cursor] prefix
git commit --amend -m "Remove temporary commit message file"

# Use rebase to modify the second-most recent commit
cat > .git/rebase-msg << EOF
Refactor project structure and enhance GTC 2025 analysis

This commit provides a major refactoring of the project structure and 
significant enhancements to the GTC 2025 analysis project:

- Reorganized project into src, data, docs, and outputs directories
- Enhanced data analysis with visualization capabilities
- Created professional narrative documents with improved design
- Added personal branding and marketing package
- Included readable alternatives for all content in multiple formats
- Updated documentation with better organization and usage instructions
- Fixed path references in all scripts

The enhanced analysis now provides deeper insights into conference trends, 
with particular focus on AI, Digital Twins, and industry-specific 
applications. The marketing package enables effective sharing of insights 
through various channels.
EOF

# Use rebase to change the parent commit message
git rebase -i --exec "git commit --amend -F .git/rebase-msg && rm .git/rebase-msg" HEAD~2 