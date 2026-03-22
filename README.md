# OPSEC Screenshot Tool

Un script en Python diseñado para usuarios que quieren eliminar la posibilidad de accidentalmente filtrar su zona horaria al compartir capturas de pantalla. 
El programa se ejecuta en segundo plano y cuando detecta un nuevo archivo en la carpeta de capturas de pantalla, detecta si es una imagen y elimina todo rastro de la hora a la que se tomó la captura

## Características

Elimina por completo los datos EXIF/IPTC copiando solo los píxeles puros.
Cambia el nombre original (que suele contener la fecha) a un código alfanumérico aleatorio (ej. `OPSEC_aB3dE9.png`).
Dibuja un rectángulo negro sólido en la esquina inferior derecha para tapar el reloj y notificaciones de Windows.
Escanea la imagen buscando patrones de tiempo (ej. `14:30` o `02:15 PM`) en chats o correos y los censura automáticamente.

## Instalación

Para que el script funcione, debes instalar los requisitos

### 1. Instalar Tesseract OCR (Obligatorio para que detecte la hora en las capturas de pantalla)
  **Linux**: ```sudo apt install tesseract-ocr``` for debian or ```sudo pacman -S tesseract tesseract-data``` for arch
  **Windows**: Instalarlo en https://github.com/UB-Mannheim/tesseract/wiki, luego de instalarlo debes poner la ruta de instalacion de tessereact dentro del script (Por defecto suele ser C:\Program Files\Tesseract-OCR\tesseract.exe)

### 2. Instalar dependencias en python
```pip install -r requirements.txt```

### Ajustes
Puedes modificar lo siguiente dentro del script:
**RUTA_TESSERACT_WINDOWS**: (Solo Windows) Pon aquí la ruta de tu tesseract.exe. Si usas Linux, déjalo vacío o bórralo.
**carpeta_manual**: Por defecto, el script busca automáticamente tu carpeta de Screenshots. Si usas una ruta personalizada, escríbela aquí (ej. carpeta_manual = "/home/ruka/femboyfurrys").
**Tamaño de la censura inferior**: Si quieres hacer el rectángulo de censura de Windows más grande o pequeño, busca la línea censura = [ancho - 300, alto - 50, ancho, alto] y modifica los valores 300 (ancho) y 50 (alto).

### Ejecucion sin consola
**En windows**: Sólo con cambiar el nombre del script de main.py a main.pyw se ejecutará sin terminal, solo q luego tendrás q cerrarlo desde el administrador de tareas
**En linux**: ```bash
nohup python3 /ruta/absoluta/a/tu/main.py > /dev/null 2>&1 &``` y luego para cerrarlo corres este comando en la terminal: ```ps aux | grep main.py``` y lo cierras con ```kill <PID>```

### Autostart
**En windows**: Primero que el archivo sea .pyw, haces un acceso directo al archivo, vas al programa "ejecutar" (win+r) y eescribes ```shell:startup``` y le das a enter, cuando se te abra una carpeta tienes que arrastrar el acceso directo ahí y listo
**En linux**: 
--Para KDE Plsma, gnome,Ubuntu...---
creas el archivo de autoinicio con```nano ~/.config/autostart/opsec.desktop``` y eescribes esto:
[Desktop Entry]
Type=Application
Name=OPSEC Screenshot
Comment=Espera y censura capturas de pantalla
Exec=python3 /ruta/absoluta/a/tu/main.py
Terminal=false
---Para HYPRLAND---
```nano ~/.config/hypr/hyprland.conf```
buscas la sección exec-once y añades esto: 
```exec-once = nohup python3 /ruta/absoluta/a/tu/main.py > /dev/null 2>&1 &```
