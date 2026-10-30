# Halo C.E con trucos (OpenCE para Android)

Versión de **Halo: Combat Evolved para Android** basada en [OpenCE (Open Community Edition)](https://github.com/OpenCommunityEdition/OpenCE), con un **menú de trucos en español** y la posibilidad de **mover las partes del HUD** (radar, escudo, vida, munición y granadas).

> Proyecto no oficial de un aficionado. No tiene relación con Microsoft, Xbox Game Studios, Halo Studios, Activision ni Bungie. Halo y Halo: Combat Evolved son marcas de Microsoft Corporation. **No incluye el juego**: necesitas tu propia copia (imagen de disco de Xbox, `.iso` o `.xiso`), como pide OpenCE.

## Qué incluye

### Menú TRUCOS
Se abre en **Settings > Player Setup > tu perfil > TRUCOS**, y en partida en **pausa > SETTINGS > TRUCOS**.

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

### HUD movible
En **TRUCOS > HUD** hay una pantalla para cada parte: radar, escudo, vida, munición y granadas. Cada una se mueve en horizontal y vertical con un ajuste **grueso** (de 100 en 100, hasta ±1000) y uno **fino** (de 5 en 5, se suma al grueso): por ejemplo, 625 es 600 y +25. Un número positivo mueve a la derecha o hacia abajo; 0 deja cada parte donde el juego la pone. La mira no se puede mover.

### Guía
En **TRUCOS > GUIA** hay una **flecha guía** con la distancia en metros, dibujada como los marcadores del juego: apunta al **aliado más cercano**, al **enemigo más cercano** o a una **bandera numerada del mapa** (las banderas son puntos que usan los scripts de cada nivel). Apunta en línea recta, no por el camino.

### Ajustes
En **TRUCOS > AJUSTES**: brillo con **HDR** (activarlo y subir la exposición ayuda cuando el juego se ve oscuro; puede bajar la fluidez), desbloquear todos los niveles de la campaña (solo para perfiles nuevos), animaciones mejoradas y bots para partidas locales de Slayer a pantalla dividida.

### Otros detalles
- La app se llama **Halo C.E**.
- Las versiones se firman siempre con la misma llave, así que cada APK nuevo **se instala encima del anterior sin borrar tu partida**.

## Cómo conseguir el APK

El APK se compila solo con **GitHub Actions** a partir del código oficial de OpenCE, al que se le aplica un parche (`trucos/trucos.patch`).

1. Entra a la pestaña **Releases** (Lanzamientos) de este repositorio.
2. Descarga el `HaloCE-trucos.apk` de la versión más reciente (marcada como "Latest").
3. Instálalo en tu celular (puede pedirte permitir instalar apps de fuentes desconocidas).

Para compilar una versión nueva: **Actions > Compilar OpenCE con trucos (APK) > Run workflow**. Por defecto usa la última versión de OpenCE; también puedes escribir una específica, por ejemplo `build-288`.

## Cómo está hecho este repositorio

Este repositorio **no es un fork** del código de OpenCE: solo guarda los cambios.

| Archivo | Para qué sirve |
|---|---|
| `.github/workflows/build-android.yml` | Descarga OpenCE, aplica los trucos, compila y publica el APK |
| `trucos/trucos.patch` | Los cambios al código de OpenCE (trucos, HUD y menús) |
| `trucos/regenerar_menus.py` | Genera las pantallas del menú y las registra |
| `trucos/header_trucos.png`, `trucos/header_hud.png` | Los títulos TRUCOS y HUD del menú |

Si OpenCE cambia las partes que toca el parche, la compilación puede fallar en el paso "Aplicar los trucos" y habrá que ajustar el parche.

## Créditos y licencia

- **OpenCE** y todo el código del juego: [OpenCommunityEdition/OpenCE](https://github.com/OpenCommunityEdition/OpenCE), bajo la licencia **GNU AGPL v3**. Los cambios de este repositorio se comparten bajo esa misma licencia.
- Menú de trucos en español, HUD movible y compilación automática: **Freed** ([@freedsny](https://github.com/freedsny)).
- Halo: Combat Evolved © Microsoft Corporation. Sin datos del juego incluidos.
