# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 11:32:41 2026
This file paints scalebars in optical microscope images, the inputs are the name of the microscope used (had 2 at the lab: "sahara" and "madagascar"; the magnification
used; the number of microns on the scalebar; and the image path
@author: hment
"""
import sys
import os
from PIL import Image, ImageDraw, ImageFont

setup = []
magnification = ['5x', '10x', '20x', '100x']

calibration = {
    'Sahara':{
        '5x':1.2671,
        '10x':2.5026,
        '20x':5.0637,  #pixeles/micra
        '100x':24.9361
        
        },
    'Madagascar':{
        '5x':1.47,
        '10x':2.91,
        '20x':5.85,
        '100x':29.4
        }
    }

def seleccionar_opcion(opciones, nombre_categoria):
    print(f"\n--- Selecciona {nombre_categoria} ---")
    lista_opciones = list(opciones)
    for i, opcion in enumerate(lista_opciones):
        print(f"{i + 1}. {opcion}")
    while True:
        try:
            seleccion = int(input(f"Elige el número: ")) - 1
            if 0 <= seleccion < len(lista_opciones):
                return lista_opciones[seleccion]
            print("❌ Número inválido.")
        except ValueError:
            print("❌ Introduce un número.")
            
def main():
    
    # --- SELECCIÓN DE DATOS ---
    nombre_microscopio = seleccionar_opcion(calibration.keys(), "Microscopio")
    mis_lentes = calibration[nombre_microscopio]
    magnificacion = seleccionar_opcion(mis_lentes.keys(), "Magnificación / Modo")
    factor = mis_lentes[magnificacion]
    print(f"\nℹ️  Factor cargado: {factor} px/µm")
    
    while True:
        try:
            largo_um = float(input("\n¿De cuántas micras (µm) quieres la barra?: "))
            if largo_um > 0: break
        except ValueError: pass

    largo_px = int(largo_um * factor)
    print(f"\n📏 Longitud de barra calculada: {largo_px} pixeles")

    # --- DIBUJAR ---
    dibujar = input("\n¿Quieres dibujar esto en una imagen ahora? (s/n): ").lower()
    
    if dibujar == 's':
        # .strip() limpia comillas y espacios molestos de Windows
        texto_usuario = input("Introduce la ruta de la imagen: ")
        ruta = texto_usuario.strip('"').strip("'").strip() 
        
        try:
            img = Image.open(ruta)
            draw = ImageDraw.Draw(img)
            w, h = img.size
            
            # --- CONFIGURACIÓN VISUAL ---
            margen_derecho =w/2.5 #1300 #600
            margen_inferior =h*0.43 #120  #80 Un poco más alto para que quepa el texto
            grosor_linea = 16
            color_escala = "white"
            tamano_fuente = 90 # Ajusta esto si el texto se ve muy grande o pequeño

            # --- COORDENADAS DE LA BARRA ---
            x_final_barra = w - margen_derecho
            x_inicio_barra = x_final_barra - largo_px
            y_barra = h - margen_inferior
            
            # 1. DIBUJAR LA LÍNEA
            draw.line([(x_inicio_barra, y_barra), (x_final_barra, y_barra)], fill=color_escala, width=grosor_linea)
            
            # --- NUEVO: AÑADIR TEXTO ---
            texto_a_escribir = f"{largo_um:g} µm" # :g quita ceros decimales innecesarios (ej: 10.0 -> 10)

            # 2. CARGAR FUENTE (Intenta cargar Arial, si falla usa la default)
            try:
                # En Windows "arial.ttf" suele funcionar directo.
                font = ImageFont.truetype("arial.ttf", tamano_fuente)
            except IOError:
                font = ImageFont.load_default()
                print("⚠️ No encontré Arial, usando fuente por defecto (se verá pequeñita).")

            # 3. CALCULAR POSICIÓN DEL TEXTO PARA CENTRARLO
            # textbbox nos da un rectángulo (left, top, right, bottom) que envuelve el texto
            bbox = draw.textbbox((0, 0), texto_a_escribir, font=font)
            texto_ancho = bbox[2] - bbox[0]
            texto_alto = bbox[3] - bbox[1]

            # Centrar horizontalmente sobre la barra
            x_texto = x_inicio_barra + (largo_px - texto_ancho) / 2
            # Ponerlo encima de la barra con un pequeño margen de 10px
            y_texto = y_barra - texto_alto - 50

            # 4. DIBUJAR EL TEXTO (A veces se dibuja un borde negro para contraste, pero empecemos simple)
            draw.text((x_texto, y_texto), texto_a_escribir, fill=color_escala, font=font)


            # --- GUARDAR ---
            dir_path, filename = os.path.split(ruta)
            nombre_salida = os.path.join(dir_path, f"escalada_{filename}")
            img.save(nombre_salida)
            print(f"\nImagen guardada como: {nombre_salida}")
            print("Revisa la carpeta, debería tener la barra y el texto centrados.")
            
        except Exception as e:
             print(f"\n❌ Algo salió mal: {e}")
             print("Revisa la ruta del archivo.")

if __name__ == "__main__":
    main()
