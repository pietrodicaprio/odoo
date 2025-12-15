#!/usr/bin/env bash
set -euo pipefail

MODULE_PATH="addons/blackship_sale"
POT_FILE="$MODULE_PATH/i18n/blackship_sale.pot"
PO_FILE="$MODULE_PATH/i18n/it.po"

failures=()

if [ ! -f "$POT_FILE" ]; then
    failures+=("Missing $POT_FILE")
fi

if [ ! -f "$PO_FILE" ]; then
    failures+=("Missing $PO_FILE")
fi

search_paths=()
for candidate in "$MODULE_PATH/models" "$MODULE_PATH/wizard"; do
    if [ -d "$candidate" ]; then
        search_paths+=("$candidate")
    fi
done

grep_for_unwrapped_errors() {
    local pattern=$1
    if [ ${#search_paths[@]} -eq 0 ]; then
        return
    fi

    local matches
    matches=$(rg --pcre2 -n "(?<!_\\()${pattern}\\(\"" "${search_paths[@]}" || true)
    if [ -n "$matches" ]; then
        failures+=("Untranslated ${pattern} found:\n$matches")
    fi
}

grep_for_unwrapped_errors "UserError"
grep_for_unwrapped_errors "ValidationError"

if [ ${#failures[@]} -ne 0 ]; then
    printf "I18n checks failed:\n" >&2
    for item in "${failures[@]}"; do
        printf "- %b\n" "$item" >&2
    done
    exit 1
fi

echo "All i18n checks passed"
