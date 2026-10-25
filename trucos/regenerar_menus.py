"""Regenera las pantallas de ajustes de OpenCE (con la pantalla CHEATS) y las
registra en menus.json. Se ejecuta desde la raiz del codigo de OpenCE, despues
de aplicar trucos.patch (tools/port_settings.py ya trae la pantalla)."""
import json
import pathlib
import sys

sys.path.insert(0, "tools")
import port_settings as ps

ce = pathlib.Path("port/assets/menus/ce")
nuevos = []
for nombre, lineas in ps.settings_files().items():
    ruta = ce / nombre
    if not ruta.exists():
        nuevos.append(nombre)
    ruta.write_text("\n".join(lineas), encoding="utf-8", newline="")

mj = pathlib.Path("port/assets/menus/menus.json")
crudo = mj.read_text(encoding="utf-8")
datos = json.loads(crudo)
archivos = datos["files"]
ancla = "ce/main_menu.settings_select.player_setup.player_profile_edit.network_setup.in_game.xml"
for nombre in nuevos:
    entrada = "ce/" + nombre
    if entrada not in archivos:
        archivos.insert(archivos.index(ancla), entrada)
mj.write_text(json.dumps(datos, indent=1, ensure_ascii=False) + ("\n" if crudo.endswith("\n") else ""), encoding="utf-8")
print("pantallas nuevas:", nuevos)
