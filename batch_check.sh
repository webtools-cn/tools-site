#!/bin/bash
# Batch fix JS syntax errors in tool HTML files
TOOLS="color-namer cors-test cron-expression-parser css-grid-generator css-grid-template-areas css-hover-animation-effects css-hover-effects css-keyframe-animation-generator css-to-js csv-join csv-to-sql curl-converter curl-to-javascript curl-to-php curl-to-python cursive-text-generator daily-affirmation-generator daily-planner days-between-dates decimal-to-hex depreciation-calculator diff-checker dns-record-comparator dockerfile-formatter dockerfile-linter donut-chart-maker drawing-tool editorconfig-generator emoji-meaning-finder emoji-search emoji-to-png exposure-calculator fancy-text-generator flexbox-layout-generator flowchart-maker focus-timer font-face-generator github-actions-generator glitch-text-generator guitar-tuner gzip-text-compressor handwriting-generator heatmap-generator hex-to-text"

for TOOL in $TOOLS; do
    echo "=== $TOOL ==="
    python3 scripts/extract_js.py "$TOOL/index.html" > "/tmp/${TOOL}.js" 2>&1
    RESULT=$(node -c "/tmp/${TOOL}.js" 2>&1)
    if echo "$RESULT" | grep -q "SyntaxError"; then
        echo "FAIL: $RESULT"
    else
        echo "OK"
    fi
done
