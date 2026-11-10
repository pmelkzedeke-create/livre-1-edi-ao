#!/usr/bin/env bash
# Repõe a mídia pesada do plugin Edit Labs AI que fica fora do git deste repositório
# (biblioteca de PNGs, exemplos, zip 3D). Baixa o mesmo commit do upstream e copia só essas pastas.
#
#   ./instalar-editlabs-midia.sh            # repõe o que faltar
#   ./instalar-editlabs-midia.sh --forcar   # copia de novo, por cima
set -euo pipefail

REPO="paullabs/edit-labs-ai"
REF="${EDITLABS_REF:-main}"          # ou um commit/tag, ex.: EDITLABS_REF=84b6129
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$RAIZ/plugins/edit-labs-ai"
PASTAS=(
  "skills/motion-vox/biblioteca"
  "skills/motion-vox/exemplo"
  "skills/explicador-vox/exemplo"
  "skills/colagem-camadas/exemplos"
  "skills/colagem-camadas/assets/3d"
)
FORCAR=0
[ "${1:-}" = "--forcar" ] && FORCAR=1

command -v git >/dev/null || { echo "Precisa do git instalado." >&2; exit 1; }
[ -d "$DEST" ] || { echo "Plugin não encontrado em $DEST" >&2; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Baixando $REPO ($REF)…"
git clone --depth 1 --branch "$REF" --filter=blob:none --sparse \
  "https://github.com/$REPO.git" "$TMP/up" >/dev/null 2>&1
git -C "$TMP/up" sparse-checkout set $(printf 'plugins/edit-labs-ai/%s ' "${PASTAS[@]}") >/dev/null 2>&1

for p in "${PASTAS[@]}"; do
  de="$TMP/up/plugins/edit-labs-ai/$p"
  para="$DEST/$p"
  if [ ! -d "$de" ]; then printf "  · %s: não existe no upstream, pulei\n" "$p"; continue; fi
  if [ -d "$para" ] && [ "$FORCAR" = 0 ]; then printf "  ✓ %s (já estava)\n" "$p"; continue; fi
  mkdir -p "$(dirname "$para")"
  cp -R "$de" "$para"
  printf "  ✓ %s\n" "$p"
done

echo "Pronto. Se o plugin já estava instalado, rode de novo:  plugins/edit-labs-ai/bin/editlabs-setup"
