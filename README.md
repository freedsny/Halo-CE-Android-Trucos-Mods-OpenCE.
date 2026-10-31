# Halo C.E con trucos (OpenCE para Android)

Versión de **Halo: Combat Evolved para Android** basada en [OpenCE (Open Community Edition)](https://github.com/OpenCommunityEdition/OpenCE), con **menús en español**, un **menú de trucos**, una **flecha guía hacia el objetivo de la misión** y la posibilidad de **mover las partes del HUD**.

Este parche de trucos se creó y se aplica sobre el repositorio oficial de OpenCE: hice un parche con los cambios y un workflow de GitHub Actions que se los aplica al código oficial de OpenCE y compila el APK.

**Creador: freddVelp ([@freedsny](https://github.com/freedsny)).**

> Proyecto no oficial de un aficionado. No tiene relación con Microsoft, Xbox Game Studios, Halo Studios, Activision ni Bungie. Halo y Halo: Combat Evolved son marcas de Microsoft Corporation. **No incluye el juego**: necesitas tu propia copia (imagen de disco de Xbox, `.iso` o `.xiso`), como pide OpenCE.

## Qué incluye

### Menús en español
El menú principal (CAMPAÑA, MULTIJUGADOR, PERFILES, AJUSTES, SALIR), los ajustes del perfil, la selección de perfil, el menú de campaña, el de multijugador y los botones (VOLVER, ACEPTAR, CANCELAR...) están en español. Algunas pantallas internas de OpenCE siguen en inglés.

### Menú TRUCOS
Se abre en **AJUSTES > tu perfil > TRUCOS**, y en partida en **pausa > AJUSTES > TRUCOS**.

| Opción | Qué hace |
|---|---|
| Munición infinita | La munición de reserva nunca se acaba |
| Sin recargar | El cargador nunca se vacía |
| Súper salto | Saltas mucho más alto |
| Modo dios | No mueres por disparos ni caídas |
| Matar de un golpe | Tus disparos matan al instante |
| Medusa | Los enemigos que te miran mueren |
| Jetpack | Puedes volar |
| Poseer al chocar | Al chocar con un enemigo o vehículo lo controlas |
| Sentir el daño de otros | Cuando otros reciben daño, tu pantalla reacciona como si te golpearan |
| Todas las armas | Caen todas las armas cerca de ti |
| Todos los vehículos | Caen en círculo alrededor de ti, separados |
| Todos los powerups | Caen todos los powerups cerca de ti |
| Camuflaje activo | Te vuelves invisible |

Las cuatro últimas funcionan como **botones**: las pones en ON, vuelves al juego, se ejecutan una vez y vuelven solas a OFF. Solo aparecen las armas, vehículos y powerups que el mapa actual tiene cargados.
Los trucos **solo funcionan en partidas que no son en red**. En el juego de otro jugador valen sus reglas.

### Flecha guía
En **TRUCOS > GUIA** hay una **flecha** con la distancia en metros, dibujada como los marcadores del juego. Puede apuntar a:

- **Objetivo de la misión**: en la campaña, la zona a la que la misión espera que llegues para avanzar. La flecha lee en vivo qué está esperando la misión, así que cambia sola cuando avanzas o cambia el objetivo, y funciona al cargar una partida guardada. Está preparada para las diez misiones de la campaña.
- **Aliado más cercano** o **enemigo más cercano**.

La flecha apunta en línea recta hacia la siguiente zona, no por el camino. Si en un momento la misión no espera que llegues a ningún lugar (por ejemplo, mientras tienes que eliminar enemigos), la flecha no aparece.

### HUD movible
En **TRUCOS > HUD** hay una pantalla para cada parte: radar, escudo, vida, munición y granadas. Cada una se mueve en horizontal y vertical con un ajuste **grueso** (de 100 en 100, hasta ±1000) y uno **fino** (de 5 en 5, se suma al grueso): por ejemplo, 625 es 600 y +25. Un número positivo mueve a la derecha o hacia abajo; 0 deja cada parte donde el juego la pone. La mira no se puede mover.

### Ajustes
En **TRUCOS > AJUSTES**:

- **Idioma del juego**: con una copia europea del juego (que trae español), los textos que vienen del disco salen en español. Cambia al reiniciar.
- **HDR, exposición y curva de tonos**: activar HDR y subir la exposición ayuda cuando el juego se ve oscuro; puede bajar la fluidez.
- **Desbloquear niveles** de la campaña (solo para perfiles nuevos).
- **Animaciones mejoradas**.
- **Bots** para partidas locales de Slayer a pantalla dividida: cantidad, nivel y equipos.

### Otros detalles
- La app se llama **Halo C.E**.
- Las versiones se firman siempre con la misma llave, así que cada APK nuevo **se instala encima del anterior sin borrar tu partida**.

## Cómo conseguir el APK

El APK se compila solo con **GitHub Actions** a partir del código oficial de OpenCE, al que se le aplica el parche (`trucos/trucos.patch`).

1. Entra a la pestaña **Releases** (Lanzamientos) de este repositorio.
2. Descarga el APK de la versión más reciente (marcada como "Latest"). Su nombre lleva la versión de OpenCE con la que se compiló, por ejemplo `HaloCE-trucos-build-335.apk`.
3. Instálalo en tu celular (puede pedirte permitir instalar apps de fuentes desconocidas).

Para compilar una versión nueva: **Actions > Compilar OpenCE con trucos (APK) > Run workflow**. Por defecto usa la última versión de OpenCE; también puedes escribir una específica, por ejemplo `build-335`.

## Cómo está hecho este repositorio

Este repositorio **no es un fork** del código de OpenCE: solo guarda los cambios.

| Archivo | Para qué sirve |
|---|---|
| `.github/workflows/build-android.yml` | Descarga OpenCE, aplica los trucos, compila y publica el APK |
| `trucos/trucos.patch` | Los cambios al código de OpenCE: trucos, flecha guía, HUD y menús |
| `trucos/regenerar_menus.py` | Genera las pantallas del menú, las registra y las pasa al español |
| `trucos/textos_es.py` | Los textos en español de los menús |
| `trucos/menu_es.py` | Dibuja en español las palabras del menú principal y los títulos |
| `trucos/header_*.png` | Los títulos TRUCOS, HUD, AJUSTES y GUIA |

Si OpenCE cambia las partes que toca el parche, la compilación puede fallar en el paso "Aplicar los trucos" y habrá que ajustar el parche.

## Créditos y licencia

- **OpenCE** y todo el código del juego: [OpenCommunityEdition/OpenCE](https://github.com/OpenCommunityEdition/OpenCE), bajo la licencia **GNU AGPL v3**. Los cambios de este repositorio se comparten bajo esa misma licencia.
- Trucos y menús en español, flecha guía, HUD movible y compilación automática: **freddVelp** ([@freedsny](https://github.com/freedsny)).
- La flecha de objetivo usa solo los nombres de los scripts de cada misión como referencia; no incluye scripts ni datos del juego.
- Halo: Combat Evolved © Microsoft Corporation.
