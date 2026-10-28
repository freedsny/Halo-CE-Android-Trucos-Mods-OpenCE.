"""Dibuja, con la fuente de OpenCE, las palabras en espanol del menu principal y
el titulo de la pantalla de perfil, iguales en estilo a las del juego. Lo usa
regenerar_menus.py (necesita pillow, numpy y scipy)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.ndimage import gaussian_filter

# ---- palabras del menu principal (1024x256, escala 4)
W, H, SCALE = 1024, 256, 4
CAP, BASELINE, MIDDLE, TRACK = 78, 102, 520, 1.0


def _font(font_path, cap):
    probe = ImageFont.truetype(font_path, 1000)
    left, top, right, bottom = probe.getbbox("H")
    return ImageFont.truetype(font_path, round(1000 * cap / (bottom - top)))


def _layer(font, text, fill, stroke=0):
    widths = [font.getlength(c) for c in text]
    x = MIDDLE - (sum(widths) + TRACK * (len(text) - 1)) / 2
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for c, w in zip(text, widths):
        draw.text((x, BASELINE), c, font=font, fill=fill, anchor="ls", stroke_width=stroke, stroke_fill=fill)
        x += w + TRACK
    return img


def item(text, state, font_path):
    """state 0: apagada (azul tenue); state 1: resaltada (blanca con brillo azul)"""
    font = _font(font_path, CAP)
    if state == 0:
        return _layer(font, text, (0x28, 0x95, 0xFF, round(0.467 * 255)))
    glow = _layer(font, text, (0x28, 0x95, 0xFF, 255), stroke=11)
    glow = glow.filter(ImageFilter.GaussianBlur(2.19 * SCALE))
    a = np.asarray(glow).copy()
    a[..., 3] = (a[..., 3] * 0.65).astype(np.uint8)
    return Image.alpha_composite(Image.fromarray(a, "RGBA"), _layer(font, text, (255, 255, 255, 255)))


# ---- titulo de pantalla (512x64 a escala 4)
def header(text, font_path, scale=4):
    left, top, cap = 30.68, 33.5, 21.5
    font = _font(font_path, cap * scale)
    width = font.getlength(text) / scale
    wide, high = 512 * scale, 64 * scale
    alpha = np.zeros((high, wide), np.float32)
    x0, y0 = 29.08 * scale, 28.05 * scale
    alpha[round(y0):round(y0 + 40.95 * scale), round(x0):round(x0 + (width + 28) * scale)] = 1
    alpha = gaussian_filter(alpha, sigma=(13.06 * scale, 14.23 * scale), mode="constant") * 0.893
    alpha[59 * scale:, :] = 0
    img = np.zeros((high, wide, 4), np.uint8)
    img[..., 0], img[..., 1], img[..., 2] = 0x02, 0x19, 0x31
    img[..., 3] = np.clip(alpha * 255 + 0.5, 0, 255).astype(np.uint8)
    image = Image.fromarray(img, "RGBA")
    cap_top = font.getbbox("H")[1]
    ImageDraw.Draw(image).text((left * scale, top * scale - cap_top), text, font=font, fill=(0x29, 0x95, 0xFD, 255))
    return image
