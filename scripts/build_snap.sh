#!/bin/bash
# =============================================================================
# build_snap.sh — Build HydrateMe snap locally and optionally push to the
#                 Snap Store.
#
# Usage:
#   ./scripts/build_snap.sh                        # Build only (LXD container)
#   ./scripts/build_snap.sh --destructive          # Build on host (no LXD)
#   ./scripts/build_snap.sh --push                 # Build + push + release
#   ./scripts/build_snap.sh --destructive --push   # Destructive build + push
#
# Prerequisites:
#   sudo snap install snapcraft --classic
#   sudo snap install lxd && sudo lxd init --auto   # (for LXD mode)
#   sudo usermod -aG lxd $USER                      # (then re-login)
#   snapcraft login                                  # (for --push)
# =============================================================================

set -e

# ── Flags ──────────────────────────────────────────────────────────────────────
PUSH=false
DESTRUCTIVE=false

for arg in "$@"; do
  case "$arg" in
    --push)        PUSH=true ;;
    --destructive) DESTRUCTIVE=true ;;
    --help|-h)
      sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown option: $arg"
      echo "Run with --help for usage."
      exit 1
      ;;
  esac
done

# ── Helpers ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

info()    { echo -e "${CYAN}[build_snap]${RESET} $*"; }
success() { echo -e "${GREEN}[build_snap] ✔ $*${RESET}"; }
error()   { echo -e "${RED}[build_snap] ✘ $*${RESET}" >&2; exit 1; }

# ── Sanity checks ──────────────────────────────────────────────────────────────
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$PROJECT_ROOT"

if ! command -v snapcraft &>/dev/null; then
  error "snapcraft is not installed. Run: sudo snap install snapcraft --classic"
fi

if [ "$DESTRUCTIVE" = false ] && ! command -v lxd &>/dev/null; then
  error "LXD is not installed. Run: sudo snap install lxd && sudo lxd init --auto
Alternatively, pass --destructive to build directly on your host."
fi

# ── Version ────────────────────────────────────────────────────────────────────
VERSION=$(grep '"version"' package.json | cut -d '"' -f 4)
info "Building HydrateMe snap v${BOLD}${VERSION}${RESET}"

# ── Build ──────────────────────────────────────────────────────────────────────
if [ "$DESTRUCTIVE" = true ]; then
  info "Mode: destructive (building directly on host)"
  snapcraft --destructive-mode
else
  info "Mode: LXD container (isolated build)"
  snapcraft --use-lxd
fi

# ── Locate built snap ──────────────────────────────────────────────────────────
SNAP_FILE=$(ls hydrateme_*.snap 2>/dev/null | head -1)

if [ -z "$SNAP_FILE" ]; then
  error "No .snap file found after build. Check snapcraft output above."
fi

success "Snap built: ${SNAP_FILE}"
echo ""
echo -e "  ${BOLD}Test locally with:${RESET}"
echo -e "    sudo snap install ${SNAP_FILE} --dangerous"
echo ""

# ── Push & Release ─────────────────────────────────────────────────────────────
if [ "$PUSH" = true ]; then
  info "Uploading ${SNAP_FILE} to the Snap Store..."

  if ! snapcraft whoami &>/dev/null; then
    error "Not logged in to the Snap Store. Run: snapcraft login"
  fi

  snapcraft upload --release=stable "$SNAP_FILE"
  success "Published to Snap Store on the 'stable' channel!"
  echo ""
  echo -e "  ${BOLD}View on the store:${RESET}"
  echo -e "    https://snapcraft.io/hydrateme"
else
  info "Skipping push. To publish, run:"
  echo -e "    snapcraft upload --release=stable ${SNAP_FILE}"
  echo -e "  or re-run with:  ${BOLD}./scripts/build_snap.sh --push${RESET}"
fi
