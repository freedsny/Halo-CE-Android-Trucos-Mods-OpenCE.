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

# 2) el titulo "TRUCOS" (imagen ya dibujada en trucos/header_trucos.png)
png = "ce/port/main_menu/settings_select/player_setup/player_profile_edit/network_setup/cheats/header_trucos.png"
bitmap = f"{ps.PE}/network_setup/cheats/header_trucos"
destino = menus / png
destino.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(aqui / "header_trucos.png", destino)

bitmaps_xml = ce / "bitmaps.xml"
texto = bitmaps_xml.read_text(encoding="utf-8")
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
if png not in archivos:
    archivos.insert(bisect.bisect_left(archivos, png), png)
mj.write_text(json.dumps(datos, indent=1, ensure_ascii=False) + ("\n" if crudo.endswith("\n") else ""),
              encoding="utf-8")

# 4) la lista SETTINGS: "NETWORK SETUP" pasa a decir TRUCOS Y RED, con su texto en espanol
strings_xml = ce / "strings.xml"
texto = strings_xml.read_text(encoding="utf-8")
cambios = [
    ('<string text="NETWORK SETUP " map="8"/>', '<string text="TRUCOS Y RED" map="8"/>'),
    ('<string text="Internet play, updates and the\\nmultiplayer HUD.\\n\\nProfile:"/>',
     '<string text="Trucos (municion infinita, super\\nsalto, modo dios...), juego en\\nlinea y HUD multijugador.\\n\\nProfile:"/>'),
]
for viejo, nuevo in cambios:
    if viejo in texto:
        texto = texto.replace(viejo, nuevo)
    else:
        print("AVISO: no se encontro el texto:", viejo)
strings_xml.write_text(texto, encoding="utf-8", newline="")
print("pantallas nuevas:", nuevos)
