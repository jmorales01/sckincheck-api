from ultralytics import YOLO
import cv2
import sys
import json

def main():
    if len(sys.argv) != 4:
        print("Uso: python analyzer.py <ruta_imagen_entrada> <ruta_resultado>")
        sys.exit(1)

    ruta_imagen_entrada = sys.argv[1]
    ruta_resultado_json = sys.argv[2]
    ruta_resultado = sys.argv[3]

    model = YOLO('best.pt')

    # Cargar la imagen
    frame = cv2.imread(ruta_imagen_entrada)
    resultados = model.predict(frame, imgsz=640)

    # Obtener información adicional de los resultados
    anotaciones = resultados[0].plot()
    detecciones = resultados[0].boxes.xyxy.numpy()
    confidencias = resultados[0].boxes.conf.numpy()
    clases = resultados[0].boxes.cls.numpy()

    cv2.imwrite(ruta_resultado, anotaciones)    #Guardar imagenes

    # Crear una lista de resultados
    resultados_deteccion = []
    for i in range(len(detecciones)):
        deteccion_info = {
            'clase': int(clases[i]),
            'coordenadas': detecciones[i].tolist(),
            'confidencia': float(confidencias[i])
        }
        resultados_deteccion.append(deteccion_info)

    # Guardar los resultados en un archivo JSON
    with open(ruta_resultado_json, 'w') as json_file:
        json.dump(resultados_deteccion, json_file, indent=4)

if __name__ == "__main__":
    main()
