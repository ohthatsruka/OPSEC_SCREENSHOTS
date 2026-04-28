# OPSEC Screenshot Tool
# Copyright (C) 2026 Ruka071
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details. 

import os
import time
import random
import string
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image, ImageDraw
import re
import pytesseract

RUTA_TESSERACT_WINDOWS = ""  # <-- Solo para Windows, lo puedes borrar si usas linux

if RUTA_TESSERACT_WINDOWS and os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = RUTA_TESSERACT_WINDOWS

# esto es para conseguir el directorio 
USER = os.path.expanduser("~")
carpeta_manual = "" # esto es por si quieres ponerle un directorio tú en vez de q lo busque el script

possible_folders = [
    os.path.join(USER, "Pictures", "Screenshots"),
    os.path.join(USER, "Imágenes", "Capturas de pantalla"),
    os.path.join(USER, "OneDrive", "Pictures", "Screenshots"),
    os.path.join(USER, "OneDrive", "Imágenes", "Capturas de pantalla")
]

screenshot_folder = None

if carpeta_manual != "":
    if os.path.exists(carpeta_manual):
        screenshot_folder = carpeta_manual
    else:
        print("Esa carpeta no existe guep")
else:
    for i in possible_folders:
        if os.path.exists(i):
            screenshot_folder = i
            break
if screenshot_folder:
    print(f"Carpeta en uso: {screenshot_folder}")
else:
    print("No encontre la carpeta aaaa un suisidio")
    def suicidarse():
        exit()
    suicidarse()
    

class Ruka071(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        screenshot_nueva = event.src_path
        
        # esto es para q no se haga un bucle infinito (si detecta su propia captura entonces nadota)
        if "OPSEC_" in screenshot_nueva:
            return
        
        
        if screenshot_nueva.lower().endswith(('.png', '.jpg', '.jpeg')):
            time.sleep(0.5)
            print(f"Oh gosh nueva captura")

            try:
                caracteres = string.ascii_letters + string.digits
                array_random = ''.join(random.choices(caracteres, k=7))
                nuevo_nombre = f"OPSEC_{array_random}.png" # Nombre random para la screenshot para q no salga el nombre en el archivo y lo de OPSEC es para q no haya bucle infinito
                ruta_nueva = os.path.join(screenshot_folder, nuevo_nombre)

                img = Image.open(screenshot_nueva)
                
                # para borrar metadatos
                img_limpia = Image.new(img.mode, img.size)
                img_limpia.paste(img) 
                
                # esto censura la barra de tareas en caso de q estes en windows si no estás pues lo borras ok
                ancho, alto = img_limpia.size
                draw = ImageDraw.Draw(img_limpia)
                
                censura = [ancho - 300, alto - 50, ancho, alto]
                draw.rectangle(censura, fill="black", outline="black")
                
                # buscar formatos de timepo
                regex_tiempo = r'\b([01]?\d|2[0-3]):[0-5]\d\b'
                try:
                    results = pytesseract.image_to_data(img_limpia, output_type=pytesseract.Output.DICT)
                    for i in range(len(results['text'])):
                        palabra = results['text'][i]
                        if re.search(regex_tiempo, palabra):
                            
                            x = results['left'][i]
                            y = results['top'][i]
                            w = results['width'][i]
                            h = results['height'][i]
                            
                            draw.rectangle([x, y, x + w, y + h], fill="black", outline="black")
                
                except pytesseract.TesseractNotFoundError:
                    print("Error: Tesseract OCR no está instalado o no se encuentra en la ruta configurada.")
                    
                img_limpia.save(ruta_nueva, "PNG")
                img.close()
                img_limpia.close()

                # Borrar screenshot OG
                time.sleep(0.2)
                os.remove(screenshot_nueva)
                print(f"Captura opseceada: {nuevo_nombre}")

            except Exception as e:
                print(f"Error unu {e}")

event_handler = Ruka071()
observer = Observer()
observer.schedule(event_handler, screenshot_folder, recursive=False)

observer.start()
print("Ya funciono xd")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n Adios unu")
    observer.stop()

observer.join()
