#!/bin/bash
#
# Shared logic for prompting the user to regenerate OpenSearch mappings.
# Sourced by post-rewrite and post-merge hooks.
#
# Expects $changed_mappings to be set by the caller.

echo ""
echo "========================================================"
echo "  OpenSearch mapping files were modified."
echo "========================================================"
echo ""
echo "Changed files:"
echo "$changed_mappings" | sed 's/^/  /'
echo ""

# Check if stdout is connected to a terminal (interactive).
if [ -t 1 ]; then
    read -r -p "Regenerate mappings now? [Y/n] " response < /dev/tty
    case "$response" in
        [nN]|[nN][oO])
            echo ""
            echo "Skipped. Run manually when ready:"
            echo "  docker compose down -v && docker compose build"
            echo "  docker compose run pyramid /scripts/pyramid/generate-opensearch-mappings.sh"
            echo ""
            exit 0
            ;;
    esac

    echo ""
    echo "Regenerating OpenSearch mappings..."
    echo ""

    docker compose down -v && docker compose build && \
        docker compose run pyramid /scripts/pyramid/generate-opensearch-mappings.sh

    if [ $? -eq 0 ]; then
        staged_files=$(git diff --name-only -- "$MAPPING_DIR" 2>/dev/null)
        if [ -n "$staged_files" ]; then
            git add "$MAPPING_DIR"/*.json
            echo ""
            echo "Staged files:"
            echo "$staged_files" | sed 's/^/  /'
            git commit -m "Regenerate OpenSearch mappings after rebase"
            echo ""
            echo "Mappings regenerated and committed."
        else
            echo ""
            echo "No mapping changes after regeneration."
        fi
    else
        echo ""
        echo "Mapping generation failed. Please regenerate manually:"
        echo "  docker compose down -v && docker compose build"
        echo "  docker compose run pyramid /scripts/pyramid/generate-opensearch-mappings.sh"
    fi
else
    # Non-interactive: just print the warning.
    echo "Run the following commands to regenerate:"
    echo "  docker compose down -v && docker compose build"
    echo "  docker compose run pyramid /scripts/pyramid/generate-opensearch-mappings.sh"
    echo ""
fi
