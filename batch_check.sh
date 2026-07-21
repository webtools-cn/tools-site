#!/bin/bash
# Batch check all 47 tools for JS syntax errors
TOOLS=(
  acronym-generator ai-tool-calling-tester apache-config-generator api-response-mocker
  api-tester audio-speed-changer bar-chart-maker base64-decode base64-encode
  beat-maker bic-checker bmr-calculator bracket-matcher business-name-generator
  character-frequency code-diff color-name color-namer cors-test
  cron-expression-parser css-grid-generator css-grid-template-areas css-hover-animation-effects
  css-hover-effects css-keyframe-animation-generator css-to-inline-styles css-to-js
  css-units-converter csv-join csv-to-sql curl-converter curl-to-javascript
  curl-to-php curl-to-python cursive-text-generator daily-affirmation-generator
  daily-planner days-between-dates decimal-to-hex diff-checker dns-record-comparator
  dockerfile-formatter dockerfile-linter donut-chart-maker drawing-tool
  editorconfig-generator emoji-meaning-finder
)

for tool in "${TOOLS[@]}"; do
  python3 scripts/extract_js.py "$tool/index.html" > "/tmp/${tool}.js" 2>/dev/null
  result=$(node -c "/tmp/${tool}.js" 2>&1)
  if [ $? -ne 0 ]; then
    echo "FAIL: $tool - $result"
  else
    echo "OK: $tool"
  fi
done
