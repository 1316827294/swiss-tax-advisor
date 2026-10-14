#!/usr/bin/env bash
# install.sh — One-line installer for swiss-tax-advisor Antigravity Skill
# Usage: curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash

set -e

REPO="https://github.com/1316827294/swiss-tax-advisor.git"
SKILL_NAME="swiss-tax-advisor"
GLOBAL_SKILLS_DIR="${HOME}/.gemini/config/skills"
DEST="${GLOBAL_SKILLS_DIR}/${SKILL_NAME}"

echo ""
echo "🇨🇭  Swiss Tax Advisor — Antigravity Skill Installer"
echo "======================================================"

# Check for git
if ! command -v git &>/dev/null; then
  echo "❌  git is required. Install it and try again."
  exit 1
fi

# Check for Python 3.10+
if ! python3 -c "import sys; assert sys.version_info >= (3,10)" 2>/dev/null; then
  echo "⚠️  Python 3.10+ is recommended. Some scripts may not work on older versions."
fi

# Create skills directory if needed
mkdir -p "${GLOBAL_SKILLS_DIR}"

if [ -d "${DEST}" ]; then
  echo "🔄  Updating existing installation at: ${DEST}"
  git -C "${DEST}" pull --ff-only
else
  echo "📥  Cloning into: ${DEST}"
  git clone --depth 1 "${REPO}" "${DEST}"
fi

echo ""
echo "✅  Installation complete!"
echo ""
echo "   Skill location: ${DEST}"
echo ""
echo "   Next steps:"
echo "   1. Restart your Antigravity session (agy or IDE)."
echo "   2. The skill 'swiss-tax-advisor' will appear in your available skills list."
echo "   3. Ask: 'Help me file my Swiss taxes for 2025.'"
echo ""
