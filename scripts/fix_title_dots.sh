#!/bin/bash
# Fix remaining · (middle dot) in EN title tags → | (pipe)
# Only operates on <title>...</title> lines
# Usage: cd /home/chison/tools-site && bash scripts/fix_title_dots.sh

fixed=0
for f in $(grep -rl '<title>[^<]*·[^<]*</title>' en/ --include="*.html"); do
  # Replace · with | inside <title> tag only
  sed -i '/<title>/{s/·/|/g}' "$f"
  ((fixed++))
done

echo "Fixed $fixed files"
