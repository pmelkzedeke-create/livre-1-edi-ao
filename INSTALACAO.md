# Edit Labs AI instalado neste repositório

Plugin [paullabs/edit-labs-ai](https://github.com/paullabs/edit-labs-ai) **2.2.0** (commit `84b6129`,
upstream `main`), copiado para cá e já preparado no ambiente.

- `plugins/edit-labs-ai/` — o plugin: 9 skills, 11 agentes, motor de colagem, banco de referências.
- `.claude-plugin/marketplace.json` — permite instalá-lo como marketplace local.
- `.claude/skills/*` — atalhos (symlinks) para cada skill, para o plugin ser reconhecido ao abrir o
  projeto.
- Programas e ambientes fora do repositório: `~/.local/share/edit-labs-ai/` (veja abaixo).

## Como usar

Peça em linguagem natural. A porta de entrada é a skill `edit-labs-ai`:

- "roda o Edit Labs AI" / "quero editar esse vídeo: `<link>`";
- "acha os melhores momentos" → você escolhe;
- "corta os momentos 1, 9 e 15" → você aprova o preview;
- "faz o vertical dos três", "faz a motion", "coloca B-roll", "renderiza e entrega".

Regras e estilos: `plugins/edit-labs-ai/README.md` e `plugins/edit-labs-ai/REGRAS.md`.

## O que ficou fora do git (mídia pesada)

O Arena limita o patch da sessão a ~128 MB e o plugin tem 131 MB, quase tudo mídia. Ficaram fora do
commit (listados no `.gitignore`): `skills/motion-vox/biblioteca/` (63 MB de PNGs), `skills/motion-vox/exemplo/`,
`skills/explicador-vox/exemplo/`, `skills/colagem-camadas/exemplos/` e `skills/colagem-camadas/assets/3d/`.
Para repor:

```bash
./instalar-editlabs-midia.sh          # baixa só essas pastas do upstream e copia para o lugar
```

Pacotes grandes opcionais (pranchas, anatomia 3D, trilhas) **não** vêm no repositório: baixe com
`plugins/edit-labs-ai/bin/editlabs-assets` (mostra tamanho e licença antes).

## Como foi preparado neste sandbox (Linux, sem apt)

`plugins/edit-labs-ai/bin/editlabs-setup` foi rodado até o fim e `editlabs-verificar` diz **tudo pronto**.
Ambientes criados em `~/.local/share/edit-labs-ai/`:

| ambiente | o que tem |
| --- | --- |
| `venv-corte` | corte-viral + decupagem (pyyaml, jsonschema, faster-whisper, opencv, numpy, Pillow) |
| `venv-motion` | motion-vox (Pillow 11.3.0, numpy 2.0.2, opencv 4.10.0.84, faster-whisper) |
| `venv-colagem` | motor de colagem (numpy, opencv, Pillow) |
| `bin/` | `ffmpeg`, `ffprobe`, `README.md` — os programas que o apt não pôde instalar |

Ajustes necessários por causa do sandbox (nada disso muda o comportamento do plugin num computador normal):

1. **ffmpeg**: ponte para o ffmpeg estático 9.0.2 do pacote pip `imageio-ffmpeg` (tem libx264).
2. **ffprobe**: ponte de emergência (`~/.local/share/edit-labs-ai/bin/ffprobe_shim.py`) que responde
   duração, dimensões, cadência e contagem de quadros via ffmpeg. Para trabalho sério, instale o
   ffprobe oficial.
3. **OpenCV**: a imagem Debian não tem `libGL.so.1`; troquei `opencv-python` por `opencv-python-headless`
   (mesma versão 4.10.0.84) nos três ambientes.
4. **deno**: ausente — o binário do GitHub Releases não passa pelo filtro de rede. Não faz falta para
   as skills de vídeo; só o que depende de deno (downloads do yt-dlp com desafio JS) fica limitado.
5. **Blender e recorte local (rembg)**: não instalados (`editlabs-setup --colagem --recorte` num
   computador normal). Sem eles: nada de 3D e o recorte cai para as ferramentas do kit.
6. `editlabs-setup` foi ajustado para não quebrar quando `biblioteca/` está ausente (avisa e segue).

Para usar os comandos numa sessão de terminal:

```bash
export PATH="$HOME/.local/share/edit-labs-ai/bin:$PATH"   # ffmpeg/ffprobe
export PATH="$PWD/plugins/edit-labs-ai/bin:$PATH"         # vch, cv-*, mv-*, clpy, editlabs-*
```

## Instalar de novo, noutro lugar

Com o Claude Code (o jeito oficial, recebe atualizações):

```
/plugin marketplace add paullabs/edit-labs-ai
/plugin install edit-labs-ai@edit-labs-ai
```

Com esta cópia local: `/plugin marketplace add /home/user/livre-1-edi-ao` e
`/plugin install edit-labs-ai@edit-labs-ai`, depois `bash plugins/edit-labs-ai/bin/editlabs-setup`.
