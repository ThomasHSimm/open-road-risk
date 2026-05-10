#!/bin/bash
# grep_extractions.sh
# Usage: bash grep_extractions.sh /path/to/literature/papers_summary/
# Scans extraction .md files for: AI model used, audit status, reliability verdict

DIR="${1:-.}"

echo "=== AI MODEL USED ==="
grep -ril "gemini\|chatgpt\|gpt-4\|gpt-3\|claude\|copilot" "$DIR"/*.md 2>/dev/null | while read f; do
    echo ""
    echo "--- $(basename $f) ---"
    grep -in "gemini\|chatgpt\|gpt-4\|gpt-3\|claude\|copilot\|extracted by\|produced by\|model used\|ai used" "$f" | head -5
done

echo ""
echo "=== AUDIT / RELIABILITY VERDICT ==="
grep -in "reliability.*high\|reliability.*medium\|reliability.*low\|audit verdict\|overall reliability\|safe to use" "$DIR"/*.md 2>/dev/null | sed 's|.*/||'

echo ""
echo "=== FILES WITH NO AI MODEL MENTIONED ==="
for f in "$DIR"/*.md; do
    if ! grep -qi "gemini\|chatgpt\|gpt-4\|gpt-3\|claude\|copilot\|extracted by\|produced by" "$f"; then
        echo "  $(basename $f)"
    fi
done

echo ""
echo "=== CONFIDENCE / UNCERTAINTY FLAGS ==="
grep -in "not stated\|unclear\|uncertain\|could not verify\|no evidence\|unverified" "$DIR"/*.md 2>/dev/null \
  | awk -F: '{print $1}' | xargs -I{} basename {} | sort | uniq -c | sort -rn \
  | head -20
echo "(count of 'not stated / uncertain' flags per file — higher = more conservative extraction)"
