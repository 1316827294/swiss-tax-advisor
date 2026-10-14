#!/usr/bin/env bash
# install.sh — Multi-platform installer for swiss-tax-advisor
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash -s -- --platform cursor
#   curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash -s -- --platform claude
#   curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash -s -- --platform all
#
# Supported --platform values:
#   agy        Antigravity (default when no flag given)
#   claude     Claude Code
#   cursor     Cursor IDE
#   cline      Cline (VSCode)
#   windsurf   Windsurf (Codeium)
#   copilot    GitHub Copilot
#   aider      Aider
#   devin      Devin
#   all        Install for ALL platforms at once

set -e

REPO="https://github.com/1316827294/swiss-tax-advisor.git"
SKILL_NAME="swiss-tax-advisor"
TMP_DIR="$(mktemp -d)"
PLATFORM="agy"   # default

# ── Parse arguments ────────────────────────────────────────────────────────────
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --platform) PLATFORM="$2"; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
  shift
done

echo ""
echo "🇨🇭  Swiss Tax Advisor — Installer"
echo "===================================="
echo "   Platform: $PLATFORM"
echo ""

# ── Prerequisite checks ────────────────────────────────────────────────────────
if ! command -v git &>/dev/null; then
  echo "❌  git is required. Install it and try again."
  exit 1
fi

if ! python3 -c "import sys; assert sys.version_info >= (3,10)" 2>/dev/null; then
  echo "⚠️  Python 3.10+ is recommended for the tax calculation scripts."
fi

# ── Clone repo to temp dir ─────────────────────────────────────────────────────
echo "📥  Fetching swiss-tax-advisor..."
git clone --depth 1 "$REPO" "$TMP_DIR/$SKILL_NAME" --quiet
echo "✅  Downloaded."
echo ""

# ── Install functions ──────────────────────────────────────────────────────────

install_agy() {
  DEST="${HOME}/.gemini/config/skills/${SKILL_NAME}"
  echo "🔧  [Antigravity] Installing to: $DEST"
  mkdir -p "${HOME}/.gemini/config/skills"
  if [ -d "$DEST" ]; then
    rm -rf "$DEST"
  fi
  cp -r "$TMP_DIR/$SKILL_NAME" "$DEST"
  echo "✅  [Antigravity] Done."
  echo "   → Restart your AGY session. The skill 'swiss-tax-advisor' will appear automatically."
  echo ""
}

install_claude() {
  DEST="$(pwd)"
  echo "🔧  [Claude Code] Copying CLAUDE.md to current project: $DEST"
  cp "$TMP_DIR/$SKILL_NAME/CLAUDE.md" "$DEST/CLAUDE.md"
  # Also copy scripts/ and references/ so Claude can actually run them
  mkdir -p "$DEST/swiss-tax-advisor"
  cp -r "$TMP_DIR/$SKILL_NAME/scripts"     "$DEST/swiss-tax-advisor/"
  cp -r "$TMP_DIR/$SKILL_NAME/references"  "$DEST/swiss-tax-advisor/"
  cp -r "$TMP_DIR/$SKILL_NAME/templates"   "$DEST/swiss-tax-advisor/"
  echo "✅  [Claude Code] Done."
  echo "   → CLAUDE.md is now in your project root. Claude Code reads it automatically."
  echo "   → Scripts are in ./swiss-tax-advisor/scripts/"
  echo "   → Note: update script paths in CLAUDE.md if you move the scripts/ folder."
  echo ""
}

install_cursor() {
  DEST="$(pwd)"
  echo "🔧  [Cursor] Installing rules to: $DEST/.cursor/rules/"
  mkdir -p "$DEST/.cursor/rules"
  cp "$TMP_DIR/$SKILL_NAME/.cursor/rules/swiss-tax-advisor.mdc" "$DEST/.cursor/rules/swiss-tax-advisor.mdc"
  mkdir -p "$DEST/swiss-tax-advisor"
  cp -r "$TMP_DIR/$SKILL_NAME/scripts"    "$DEST/swiss-tax-advisor/"
  cp -r "$TMP_DIR/$SKILL_NAME/references" "$DEST/swiss-tax-advisor/"
  cp -r "$TMP_DIR/$SKILL_NAME/templates"  "$DEST/swiss-tax-advisor/"
  echo "✅  [Cursor] Done."
  echo "   → .cursor/rules/swiss-tax-advisor.mdc added. Cursor reads this automatically."
  echo "   → Scripts are in ./swiss-tax-advisor/scripts/"
  echo ""
}

install_cline() {
  DEST="$(pwd)"
  echo "🔧  [Cline] Copying .clinerules to current project: $DEST"
  cp "$TMP_DIR/$SKILL_NAME/.clinerules" "$DEST/.clinerules"
  mkdir -p "$DEST/swiss-tax-advisor"
  cp -r "$TMP_DIR/$SKILL_NAME/scripts"    "$DEST/swiss-tax-advisor/"
  cp -r "$TMP_DIR/$SKILL_NAME/references" "$DEST/swiss-tax-advisor/"
  cp -r "$TMP_DIR/$SKILL_NAME/templates"  "$DEST/swiss-tax-advisor/"
  echo "✅  [Cline] Done."
  echo "   → .clinerules is now in your project root. Cline reads it automatically."
  echo ""
}

install_windsurf() {
  DEST="$(pwd)"
  echo "🔧  [Windsurf] Copying .windsurfrules to current project: $DEST"
  cp "$TMP_DIR/$SKILL_NAME/.windsurfrules" "$DEST/.windsurfrules"
  mkdir -p "$DEST/swiss-tax-advisor"
  cp -r "$TMP_DIR/$SKILL_NAME/scripts"    "$DEST/swiss-tax-advisor/"
  cp -r "$TMP_DIR/$SKILL_NAME/references" "$DEST/swiss-tax-advisor/"
  cp -r "$TMP_DIR/$SKILL_NAME/templates"  "$DEST/swiss-tax-advisor/"
  echo "✅  [Windsurf] Done."
  echo "   → .windsurfrules is now in your project root. Windsurf reads it automatically."
  echo ""
}

install_copilot() {
  DEST="$(pwd)"
  echo "🔧  [GitHub Copilot] Copying copilot-instructions.md to: $DEST/.github/"
  mkdir -p "$DEST/.github"
  cp "$TMP_DIR/$SKILL_NAME/.github/copilot-instructions.md" "$DEST/.github/copilot-instructions.md"
  mkdir -p "$DEST/swiss-tax-advisor"
  cp -r "$TMP_DIR/$SKILL_NAME/scripts"    "$DEST/swiss-tax-advisor/"
  cp -r "$TMP_DIR/$SKILL_NAME/references" "$DEST/swiss-tax-advisor/"
  cp -r "$TMP_DIR/$SKILL_NAME/templates"  "$DEST/swiss-tax-advisor/"
  echo "✅  [Copilot] Done."
  echo "   → .github/copilot-instructions.md added. Copilot Workspace reads it automatically."
  echo "   ⚠️  Note: GitHub Copilot Chat cannot execute terminal commands."
  echo "      Use it for guidance, then run scripts manually."
  echo ""
}

install_aider() {
  DEST="$(pwd)"
  echo "🔧  [Aider] Copying CONVENTIONS.md to current project: $DEST"
  cp "$TMP_DIR/$SKILL_NAME/CONVENTIONS.md" "$DEST/CONVENTIONS.md"
  mkdir -p "$DEST/swiss-tax-advisor"
  cp -r "$TMP_DIR/$SKILL_NAME/scripts"    "$DEST/swiss-tax-advisor/"
  cp -r "$TMP_DIR/$SKILL_NAME/references" "$DEST/swiss-tax-advisor/"
  cp -r "$TMP_DIR/$SKILL_NAME/templates"  "$DEST/swiss-tax-advisor/"
  echo "✅  [Aider] Done."
  echo "   → CONVENTIONS.md is now in your project root."
  echo "   → Run aider with: aider --conventions CONVENTIONS.md"
  echo ""
}

install_devin() {
  DEST="$(pwd)"
  echo "🔧  [Devin] Copying DEVIN.md to current project: $DEST"
  cp "$TMP_DIR/$SKILL_NAME/DEVIN.md" "$DEST/DEVIN.md"
  mkdir -p "$DEST/swiss-tax-advisor"
  cp -r "$TMP_DIR/$SKILL_NAME/scripts"    "$DEST/swiss-tax-advisor/"
  cp -r "$TMP_DIR/$SKILL_NAME/references" "$DEST/swiss-tax-advisor/"
  cp -r "$TMP_DIR/$SKILL_NAME/templates"  "$DEST/swiss-tax-advisor/"
  echo "✅  [Devin] Done."
  echo "   → DEVIN.md is now in your project root."
  echo ""
}

# ── Dispatch ───────────────────────────────────────────────────────────────────
case "$PLATFORM" in
  agy)       install_agy ;;
  claude)    install_claude ;;
  cursor)    install_cursor ;;
  cline)     install_cline ;;
  windsurf)  install_windsurf ;;
  copilot)   install_copilot ;;
  aider)     install_aider ;;
  devin)     install_devin ;;
  all)
    install_agy
    install_claude
    install_cursor
    install_cline
    install_windsurf
    install_copilot
    install_aider
    install_devin
    ;;
  *)
    echo "❌  Unknown platform: $PLATFORM"
    echo "    Valid options: agy, claude, cursor, cline, windsurf, copilot, aider, devin, all"
    exit 1
    ;;
esac

# ── Cleanup ────────────────────────────────────────────────────────────────────
rm -rf "$TMP_DIR"

echo "🎉  Installation complete!"
echo "    GitHub: https://github.com/1316827294/swiss-tax-advisor"
echo ""
