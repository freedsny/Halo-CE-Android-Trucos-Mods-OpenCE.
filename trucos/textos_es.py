"""Los textos en espanol de los menus de OpenCE (sin acentos: la fuente del juego).
Cada bloque va en el mismo orden que sus textos en tools/../strings.xml; None deja
el texto como esta. Lo usa regenerar_menus.py. El ancho de cada linea se calculo
con una medida calibrada con capturas, para que quepa en su espacio."""

# nombre del bloque en strings.xml -> (tipo de espacio, textos en orden)
BLOQUES = {
    "strings/common_button_captions": ("btn", [
        "VOLVER", "ACEPTAR", "CANCELAR", "RESTABLECER", "CREAR NUEVO", "BORRAR", "AVANZADO", "Perfil:"]),
    "main_menu/multiplayer_type_select/multiplayer_options": ("list", [
        "UNIRSE A PARTIDA", "CREAR PARTIDA", "INTERNET", "LAN", "ENLACE DIRECTO", "EDITAR MODOS",
        "BUSCAR SERVIDOR", "HISTORIA COOP"]),
    "main_menu/multiplayer_type_select/multiplayer_option_descriptions": ("desc", [
        "Busca partidas en\nInternet.",
        "Unete a una partida\nmultijugador en tu red local.",
        "Unete a una partida con su\nenlace de invitacion o con\nuna invitacion de Discord.",
        "Crea una partida en Internet:\nlos jugadores entran con su\nenlace o por Discord.",
        "Crea una partida solo en tu\nred local.",
        "Juega el modo historia con\nun amigo en pantalla dividida:\nel jugador 2 con un mando.",
        "Ajusta todos los detalles de\ntus modos de juego\nmultijugador y guardalos\npara usarlos despues."]),
    "main_menu/player_profiles_select/difficulty_names": ("label", ["Facil", "Normal", "Heroico", "Legendario"]),
    "main_menu/player_profiles_select/empty_profile_selected": ("desc", [
        "Elegiste un espacio\nde perfil vacio.\nQuieres crear un\nperfil nuevo?"]),
    "main_menu/player_profiles_select/joystick_set_defaults_descriptions": ("label", ["Normal", "Invertido"]),
    "main_menu/player_profiles_select/profile_description_labels": ("label", [
        "Nivel actual:", "Dificultad:", "Controles:", None, "Crear nuevo\nperfil", "Espacio\nvacio"]),
}

# imagenes: (carpeta bajo ce/shell/main_menu, nombre, palabra)
ITEMS = [
    ("campaign_select", "item_continue", "CONTINUAR"),
    ("campaign_select", "item_new_campaign", "NUEVO JUEGO"),
    ("campaign_select", "item_load_game", "CARGAR JUEGO"),
    ("campaign_select", "item_back", "VOLVER"),
]
# titulos de pantalla: (ruta bajo ce/shell/main_menu, texto)
TITULOS = [
    ("campaign_select/header_load_game__0.png", "CARGAR JUEGO"),
    ("player_profiles_select/header_select_profile__0.png", "SELECCIONAR PERFIL"),
    ("multiplayer_type_select/header_multiplayer__0.png", "MULTIJUGADOR"),
]
