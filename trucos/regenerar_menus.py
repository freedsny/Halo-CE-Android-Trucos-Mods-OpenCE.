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
sys.path.insert(0, str(aqui))
pe = ps.PE
menus = pathlib.Path("port/assets/menus")
ce = menus / "ce"

# 1) las pantallas de ajustes (incluida TRUCOS)
nuevos = []
for nombre, lineas in ps.settings_files().items():
    ruta = ce / nombre
    if not ruta.exists():
        nuevos.append(nombre)
    ruta.write_text("\n".join(lineas), encoding="utf-8", newline="")

# 2) los titulos "TRUCOS", "HUD", "AJUSTES" y "GUIA" (imagenes ya dibujadas en trucos/)
carpeta_png = "ce/port/main_menu/settings_select/player_setup/player_profile_edit/network_setup/cheats/"
titulos = [("header_trucos", f"{ps.PE}/network_setup/cheats/header_trucos"),
           ("header_hud", f"{ps.PE}/network_setup/cheats/header_hud"),
           ("header_ajustes", f"{ps.PE}/network_setup/cheats/header_ajustes"),
           ("header_guia", f"{ps.PE}/network_setup/cheats/header_guia")]
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


def traducir(texto, bloque, pares):
    """cambia, solo dentro del bloque <strings name=...bloque>, cada texto por su traduccion"""
    inicio = texto.index(f'<strings name="{pe}/{bloque}"')
    fin = texto.index("</strings>", inicio)
    parte = texto[inicio:fin]
    for viejo, nuevo in pares:
        if viejo in parte:
            parte = parte.replace(viejo, nuevo)
        else:
            print("AVISO: no se encontro:", viejo)
    return texto[:inicio] + parte + texto[fin:]


# 5) la lista SETTINGS y sus descripciones, en espanol (sin acentos: la fuente del juego)
texto = traducir(texto, "profile_edit_options", [
    ('text="CHANGE NAME"', 'text="CAMBIAR NOMBRE"'),
    ('text="CONTROLS SETUP"', 'text="CONTROLES"'),
    ('text="GAMEPADS"', 'text="MANDOS"'),
    ('text="MOUSE SETUP"', 'text="RATON"'),
    ('text="AUDIO SETUP"', 'text="AUDIO"'),
    ('text="VIDEO SETUP"', 'text="VIDEO"'),
    ('text="CHANGE COLOR"', 'text="CAMBIAR COLOR"'),
    ('text="SAVE CHANGES "', 'text="GUARDAR CAMBIOS"'),
    ('text="NETWORK SETUP "', 'text="RED"'),
])
texto = traducir(texto, "profile_edit_descriptions", [
    (r'text="Rename this profile.\n\n\nProfile:"', r'text="Cambia el nombre de este perfil.\n\n\nPerfil:"'),
    (r'text="Choose the keys and mouse\nbuttons for each action.\n\nProfile:"',
     r'text="Elige las teclas y botones del\nraton para cada accion.\n\nPerfil:"'),
    (r'text="Set this profile' + "'" + r's controller\nsensitivity and layouts.\n\nProfile:"',
     r'text="Ajusta la sensibilidad y la\ndistribucion del mando.\n\nPerfil:"'),
    (r'text="Adjust the mouse' + "'" + r's sensitivity\nand aiming.\n\nProfile:"',
     r'text="Ajusta la sensibilidad del\nraton y la punteria.\n\nPerfil:"'),
    (r'text="Adjust the volume of the music\nand of everything else.\n\nProfile:"',
     r'text="Ajusta el volumen de la musica\ny de todo lo demas.\n\nPerfil:"'),
    (r'text="Choose a window or the full\nscreen, the frame rate and more.\n\nProfile:"',
     r'text="Elige ventana o pantalla\ncompleta, los cuadros y mas.\n\nPerfil:"'),
    (r'text="Internet play, updates and the\nmultiplayer HUD.\n\nProfile:"',
     r'text="Juego por internet, buscar\nactualizaciones y el HUD.\n\nPerfil:"'),
    (r'text="Change the current profile' + "'" + r's\nfree-for-all multiplayer color.\n\nProfile:"',
     r'text="Cambia el color de este perfil\nen partidas todos contra todos.\n\nPerfil:"'),
    (r'\n\nProfile:"/>', r'\n\nPerfil:"/>'),
])
strings_xml.write_text(texto, encoding="utf-8", newline="")

# 4b) la lista de palabras de guide.mode (TRUCOS, GUIA) en port_config.c: va aqui y no en el
# parche, porque la linea vecina cambia entre versiones de OpenCE
config_c = pathlib.Path("port/linux/src/port_config.c")
fuente_c = config_c.read_text(encoding="utf-8")
palabras = '\t{ "guide.mode", { "off", "objective", "ally", "enemy", NULL }, NULL },\n'
if '"guide.mode", {' not in fuente_c:
    for punto in ('\t{ "display.hud_button_style", {', "config_words[] =\n{\n"):
        i = fuente_c.find(punto)
        if i != -1:
            if punto.startswith("config_words"):
                i += len(punto)
            fuente_c = fuente_c[:i] + palabras + fuente_c[i:]
            config_c.write_text(fuente_c, encoding="utf-8", newline="")
            break
    else:
        print("AVISO: no se encontro donde poner la lista de palabras de guide.mode")

# 5b) los otros bloques de textos (botones, multijugador, seleccion de perfil), en el orden de cada bloque
import re
import textos_es


def traducir_orden(texto, nombre, nuevos):
    inicio = texto.index(f'<strings name="{nombre}"')
    fin = texto.index("</strings>", inicio)
    cuenta = iter(nuevos)

    def cambiar(m):
        nuevo = next(cuenta)
        return m.group(0) if nuevo is None else f'<string text="{nuevo}"'.replace("\n", "\\n")

    return texto[:inicio] + re.sub(r'<string text="[^"]*"', cambiar, texto[inicio:fin]) + texto[fin:]


texto = strings_xml.read_text(encoding="utf-8")
for nombre, (tipo, textos_nuevos) in textos_es.BLOQUES.items():
    texto = traducir_orden(texto, nombre, textos_nuevos)
strings_xml.write_text(texto, encoding="utf-8", newline="")

# 6) las palabras del menu principal y el titulo de la pantalla de perfil, dibujadas en espanol
# (si faltan pillow, numpy o scipy, el menu queda en ingles y solo se avisa)
try:
    import menu_es
    fuente = "port/assets/fonts/OpenCE-Regular.ttf"
    principal = ce / "shell/main_menu"
    for archivo, palabra in (("load_campaign", "CAMPAÑA"), ("multiplayer", "MULTIJUGADOR"),
                             ("profile", "PERFILES"), ("settings", "AJUSTES"), ("quit", "SALIR")):
        for estado in (0, 1):
            menu_es.item(palabra, estado, fuente).save(principal / f"menu_{archivo}__{estado}.png", optimize=True)
    menu_es.header("AJUSTES DEL PERFIL", fuente).save(
        ce / "shell/main_menu/settings_select/player_setup/player_profile_edit/header_edit_profile_settings__0.png",
        optimize=True)
    for carpeta, nombre, palabra in textos_es.ITEMS:
        for estado in (0, 1):
            menu_es.item(palabra, estado, fuente).save(principal / carpeta / f"{nombre}__{estado}.png", optimize=True)
    for ruta, titulo in textos_es.TITULOS:
        menu_es.header(titulo, fuente).save(principal / ruta, optimize=True)
    print("menu en espanol: dibujado")
except ImportError as error:
    print("AVISO: el menu queda en ingles, falta:", error)
print("pantallas nuevas:", nuevos)
