#!/usr/bin/env python3
"""Amostra: cena de motion editorial (identidade motion-vox) montada quadro a quadro, sem footage.

Usa kit/voxlab direto: papel, asset recortado com sombra, etiqueta amarela, seta desenhada à mão,
disco amarelo atrás e pessoa de traço. Cada quadro é a mesma timeline avaliada num frame.
"""
import subprocess
from pathlib import Path

from kit import *          # noqa: F401,F403
import kit as K
import voxlab as V

SAIDA = Path("12_master"); SAIDA.mkdir(exist_ok=True)
FPS, DUR = 24, 4.0
N = int(FPS * DUR)


def quadro(frame: int):
    c = K.bg_paper()                                  # BG_PAPER
    t = frame / FPS
    p_relogio = V.ease(min(1.0, t / 0.9))
    p_disco = V.ease(min(1.0, max(0.0, (t - 0.25) / 0.6)))
    p_seta = V.ease_draw(min(1.0, max(0.0, (t - 0.9) / 1.1)))
    p_etiqueta = V.ease(min(1.0, max(0.0, (t - 1.7) / 0.5)))
    p_pessoa = V.ease(min(1.0, max(0.0, (t - 2.2) / 0.9)))

    # disco amarelo ATRÁS do herói, centrado no relógio
    CX, CY = 540, 640
    disco = Image.new("RGBA", (760, 760), (0, 0, 0, 0))
    dr = ImageDraw.Draw(disco)
    r = int(355 * p_disco)
    if r > 2:
        dr.ellipse([380 - r, 380 - r, 380 + r, 380 + r], fill=V.YELLOW + (255,))
    K.place(c, disco, (CX - 380 - 20, CY - 380 - 30), shadow=None, kind="flat")

    # herói: relógio do kit (ponteiro varre, entra em voo)
    esc = 0.88 + 0.12 * p_relogio
    larg = int(660 * esc)
    relogio, centro, raio = K.clock_at(minutes=44 + 60 * t * 0.7, width=larg, rotation=-5 + 2.5 * t)
    K.place(c, relogio, (CX - centro[0], CY - centro[1]), shadow=K.SH_PAPER, kind="obj", boil_seed=3)

    # seta à mão apontando o mostrador (vem de cima à esquerda)
    seta = V.hand_arrow((560, 340), [(80, 300), (250, 210), (470, 90)], progress=p_seta, width=9)
    if seta is not None:
        K.place(c, seta, (330, 1010), shadow=None, kind="ink")

    # etiqueta amarela, abaixo do relógio, medindo para não passar da margem
    if p_etiqueta > 0.02:
        txt = "PERDE 12 MIN"
        fs = 92
        while V.text_width(txt, V.F_BLACK, fs) > 880 and fs > 40:
            fs -= 4
        etq = K.yellow_label(c.size, txt, fontsize=fs, progress=p_etiqueta, xy=(540, 1120))
        K.place(c, etq, (0, 0), shadow=K.SH_PAPER, kind="flat")

    # pessoa de traço embaixo, à esquerda
    if p_pessoa > 0.02:
        pes, _ = V.persona((470, 560), 235, 290, height=440, pose="point", progress=p_pessoa)
        K.place(c, pes, (70, 1320), shadow=None, kind="ink")

    # texto de apoio, centralizado e medido
    if p_pessoa > 0.4:
        tit_txt = "TODO DIA"
        fsz = 104
        while V.text_width(tit_txt, V.F_BLACK, fsz) > 470 and fsz > 40:
            fsz -= 4
        tit = V.text_layer(c.size, tit_txt, V.F_BLACK, fsz, (600, 1520), color=V.INK,
                           progress=min(1.0, (p_pessoa - 0.4) / 0.4))
        K.place(c, tit, (0, 0), shadow=None, kind="ink")

    return V.finish(c, **K.FX_PLATE)


if __name__ == "__main__":
    tmp = Path("11_qa/_amostra"); tmp.mkdir(parents=True, exist_ok=True)
    for i in range(N):
        quadro(i).convert("RGB").save(tmp / f"f{i:04d}.png")
    mp4 = SAIDA / "AMOSTRA_motion_sem_footage.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                    "-i", str(tmp / "f%04d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "20", str(mp4)], check=True)
    print(mp4.resolve(), mp4.stat().st_size // 1024, "KB")
