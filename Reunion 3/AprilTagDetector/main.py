import cv2
import apriltag

# Cargar la imagen en escala de grises
ruta_imagen = "Apriltags_print/right_dataset_1cm.jpg"
imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

# Crear el detector de AprilTags
opciones = apriltag.DetectorOptions(families="tag16h5", quad_decimate=1.0) # importante aclarar la familia de tags!!!
detector = apriltag.Detector(options=opciones)

# Detectar los tags en la imagen
resultados = detector.detect(imagen)

if len(resultados) > 0:
    print(f"Se detectaron {len(resultados)} AprilTags.")
else:
    print("No se detectaron AprilTags en la imagen.")

# Dibujar los resultados en la imagen original
imagen_color = cv2.imread(ruta_imagen)  # Leer la imagen en color para visualizar resultados

for r in resultados:
    # Obtener los puntos de las esquinas del AprilTag
    esquinas = r.corners
    for i in range(4):
        pt1 = tuple(esquinas[i].astype(int))
        pt2 = tuple(esquinas[(i + 1) % 4].astype(int))
        cv2.line(imagen_color, pt1, pt2, (0, 255, 0), 2)

    # Dibujar el centro del AprilTag
    centro = tuple(r.center.astype(int))
    cv2.circle(imagen_color, centro, 5, (0, 0, 255), -1)

    # Escribir el ID del AprilTag detectado
    id_tag = r.tag_id
    cv2.putText(imagen_color, f"ID: {id_tag}", (centro[0] + 10, centro[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# Mostrar la imagen con los resultados
cv2.imshow("Detección de AprilTags", imagen_color)
cv2.waitKey(1000)
cv2.destroyAllWindows()
