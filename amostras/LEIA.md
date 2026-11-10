# Amostra de motion (identidade motion-vox) — só o motor, sem footage

`AMOSTRA_motion_editlabs.mp4` — 4 s, 1080x1920, 24 fps, 1,6 MB. Não é um vídeo entregável: é a
**prova de que o motor do plugin renderiza neste ambiente**. A cena foi escrita com `kit`/`voxlab`
(script em `amostra_motion.py`): papel de fundo, relógio do kit com ponteiro animado, disco amarelo
atrás, seta de marcador desenhada progressivamente, etiqueta amarela e persona de traço entrando
traço por traço, com boil e grain da identidade.

Render: `~/.../plugins/edit-labs-ai/bin/mvpy amostra_motion.py` (~3min20 para 96 quadros; o boil e o
finish são o custo).

Para o trabalho de verdade, a motion-vox parte de um vertical já cortado (`00_brief/fonte.mp4`) e
ancora cada evento numa palavra do transcript.
