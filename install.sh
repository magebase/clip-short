#!/usr/bin/env bash
# ==============================================================================
# clip-short: Universal Multi-Agent CLI Skills Installer
# Links clip-short into all supported agent CLIs (agy, claude, codex, cursor, etc.)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="clip-short"

echo "==================================================================="
echo " Installing skill [${SKILL_NAME}] from ${SCRIPT_DIR}"
echo "==================================================================="

# List of well-known agent CLI skills directories
TARGET_DIRS=(
  # Antigravity CLI & Gemini Agents
  "${HOME}/.gemini/config/skills"
  "${HOME}/.gemini/skills"
  "${HOME}/.gemini/antigravity/skills"
  "${HOME}/.gemini/antigravity-cli/skills"

  # Universal Agent standard & Factory
  "${HOME}/.agents/skills"
  "${HOME}/.factory/skills"

  # Claude Code
  "${HOME}/.claude/skills"

  # Cursor, Codex & Copilot
  "${HOME}/.cursor/skills"
  "${HOME}/.codex/skills"
  "${HOME}/.copilot/skills"

  # Windsurf / Codeium & OpenHands
  "${HOME}/.codeium/windsurf/skills"
  "${HOME}/.openhands/skills"

  # Config-based agent frameworks
  "${HOME}/.config/agents/skills"
  "${HOME}/.config/opencode/skills"
  "${HOME}/.config/devin/skills"
  "${HOME}/.config/crush/skills"
  "${HOME}/.config/goose/skills"
  "${HOME}/.goose/skills"
  "${HOME}/.continue/skills"

  # Additional agent CLI environments
  "${HOME}/.crush/skills"
  "${HOME}/.roo/skills"
  "${HOME}/.reasonix/skills"
  "${HOME}/.codestudio/skills"
  "${HOME}/.terramind/skills"
  "${HOME}/.kode/skills"
  "${HOME}/.vibe/skills"
  "${HOME}/.hermes/skills"
)

LINKED_COUNT=0

for dir in "${TARGET_DIRS[@]}"; do
  # If the parent tool directory exists or if it's a primary agent framework, link it
  parent_agent_dir="$(dirname "$dir")"
  if [ -d "$parent_agent_dir" ] || [[ "$dir" == *".gemini"* ]] || [[ "$dir" == *".agents"* ]] || [[ "$dir" == *".claude"* ]]; then
    mkdir -p "$dir"
    target_link="${dir}/${SKILL_NAME}"
    rm -rf "$target_link" 2>/dev/null || true
    ln -s "$SCRIPT_DIR" "$target_link"
    echo "  [✓] Linked to ${target_link}"
    LINKED_COUNT=$((LINKED_COUNT + 1))
  fi
done

# If invoked inside a git repository with an .agents folder, link locally as well
if [ -d ".agents" ]; then
  mkdir -p ".agents/skills"
  rm -rf ".agents/skills/${SKILL_NAME}" 2>/dev/null || true
  ln -s "$SCRIPT_DIR" ".agents/skills/${SKILL_NAME}"
  echo "  [✓] Linked locally to .agents/skills/${SKILL_NAME}"
  LINKED_COUNT=$((LINKED_COUNT + 1))
fi

echo "==================================================================="
echo " Successfully installed [${SKILL_NAME}] across ${LINKED_COUNT} agent CLI environments!"
echo "==================================================================="
