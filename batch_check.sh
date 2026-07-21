#!/bin/bash
cd /home/chison/tools-site

TOOLS=(
pdf-page-extractor pdf-to-excel pdf-to-html pdf-to-jpg pdf-to-ppt piano-keyboard
pie-chart-maker privacy-policy-generator properties-to-yaml quiz-generator
radar-chart-maker random-password-generator receipt-generator
regex-character-class-generator regex-cheatsheet rot13-converter
scatter-plot-maker schema-generator seo-meta-generator shopping-list-generator
sitemap-validator snake-game social-share-link-generator spectrum-analyzer
sql-migration-generator sql-to-csv sql-to-json sql-to-kysely sql-to-prisma
svg-color-changer svg-to-data-uri swot-analysis-generator tdee-calculator
terms-generator text-diff-checker text-normalizer text-palindrome-checker
text-readability-analyzer text-sentiment-analyzer text-to-braille tic-tac-toe
tsv-to-csv unique-id-generator username-generator video-compress
vite-config-generator whois-lookup word-search-generator word-to-pdf
workout-generator yes-no-generator
)

for tool in "${TOOLS[@]}"; do
    html="$tool/index.html"
    if [ ! -f "$html" ]; then
        echo "SKIP: $tool - no index.html"
        continue
    fi
    python3 scripts/extract_js.py "$html" > "/tmp/${tool}.js" 2>/dev/null
    result=$(node -c "/tmp/${tool}.js" 2>&1)
    if [ $? -eq 0 ]; then
        echo "OK: $tool"
    else
        echo "ERR: $tool - $result"
    fi
done
