"""Regenera las pantallas de ajustes de OpenCE (con la pantalla TRUCOS), pone
su titulo y los textos en espanol, y las registra en menus.json y bitmaps.xml.
Se ejecuta desde la raiz del codigo de OpenCE, despues de aplicar
trucos.patch (tools/port_settings.py ya trae la pantalla)."""
import bisect
import json
import pathlib
import shutil
import sys

sys.path.insert(0, "tools")
import port_settings as ps

aqui = pathlib.Path(__file__).resolve().parent
menus = pathlib.Path("port/assets/menus")
ce = menus / "ce"

# 1) las pantallas de ajustes (incluida TRUCOS)
nuevos = []
for nombre, lineas in ps.settings_files().items():
    ruta = ce / nombre
    if not ruta.exists():
        nuevos.append(nombre)
    ruta.write_text("\n".join(lineas), encoding="utf-8", newline="")

# 2) los titulos "TRUCOS", "HUD" y "AJUSTES" (imagenes ya dibujadas en trucos/)
carpeta_png = "ce/port/main_menu/settings_select/player_setup/player_profile_edit/network_setup/cheats/"
titulos = [("header_trucos", f"{ps.PE}/network_setup/cheats/header_trucos"),
           ("header_hud", f"{ps.PE}/network_setup/cheats/header_hud"),
           ("header_ajustes", f"{ps.PE}/network_setup/cheats/header_ajustes")]
pngs = []
bitmaps_xml = ce / "bitmaps.xml"
texto = bitmaps_xml.read_text(encoding="utf-8")
for nombre, bitmap in titulos:
    png = f"{carpeta_png}{nombre}.png"
    pngs.append(png)
    destino = menus / png
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(aqui / f"{nombre}.png", destino)
    if f'name="{bitmap}"' not in texto:
        entrada = (f'\t<bitmap name="{bitmap}">\n'
                   f'\t\t<frame png="{png}" width="512" height="64"/>\n'
                   f'\t</bitmap>\n')
        fin = texto.rindex("</menus>")
        texto = texto[:fin] + entrada + texto[fin:]
bitmaps_xml.write_text(texto, encoding="utf-8", newline="")

# 3) menus.json: las pantallas nuevas y el titulo
mj = menus / "menus.json"
crudo = mj.read_text(encoding="utf-8")
datos = json.loads(crudo)
archivos = datos["files"]
ancla = "ce/main_menu.settings_select.player_setup.player_profile_edit.network_setup.in_game.xml"
for nombre in nuevos:
    entrada = "ce/" + nombre
    if entrada not in archivos:
        archivos.insert(archivos.index(ancla), entrada)
for png in pngs:
    if png not in archivos:
        archivos.insert(bisect.bisect_left(archivos, png), png)
mj.write_text(json.dumps(datos, indent=1, ensure_ascii=False) + ("\n" if crudo.endswith("\n") else ""),
              encoding="utf-8")

# 4) la lista SETTINGS: el ultimo item (ABOUT) pasa a ser TRUCOS y abre su pantalla
pe = ps.PE
lista = ce / "main_menu.settings_select.player_setup.player_profile_edit.xml"
texto = lista.read_text(encoding="utf-8")
ancla = f'<widget name="{pe}/about_item"'
inicio = texto.index(ancla)
fin = texto.index("</widget>", inicio)
bloque = texto[inicio:fin]
viejo = '<on event="left_mouse" run="NULL"/>'
assert viejo in bloque, "no se encontro el item ABOUT"
pantalla = f"{pe}/network_setup/cheats/cheats_settings_screen"
nuevo = (f'<on event="a" open="{pantalla}"/>\n\t\t<on event="start" open="{pantalla}"/>\n'
         '\t\t<on event="left_mouse" run="mouse emit accept event"/>')
lista.write_text(texto[:inicio] + bloque.replace(viejo, nuevo) + texto[fin:], encoding="utf-8", newline="")

strings_xml = ce / "strings.xml"
texto = strings_xml.read_text(encoding="utf-8")
cambios = [
    ('<string text="ABOUT" map="9"/>', '<string text="TRUCOS" map="9"/>'),
    ('<string text="Halo: Combat Evolved, the Xbox\\ngame, on this computer.\\n\\nProfile:"/>',
     '<string text="Trucos, armas y vehiculos,\\ny mover partes del HUD.\\n\\nProfile:"/>'),
]
for viejo, nuevo in cambios:
    assert viejo in texto, "no se encontro el texto: " + viejo
    texto = texto.replace(viejo, nuevo)
strings_xml.write_text(texto, encoding="utf-8", newline="")
print("pantallas nuevas:", nuevos)
