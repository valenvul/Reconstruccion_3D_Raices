import open3d as o3d
import os

# Ruta del archivo .ply
archivo = input("Nube de puntos: ")
carpeta = "results/"
file_path = os.path.join(carpeta, archivo)

# Cargar la nube de puntos desde el archivo .ply
point_cloud = o3d.io.read_point_cloud(file_path)

# Verificar si se cargó correctamente
if not point_cloud.is_empty():
    print(f"Nube de puntos cargada exitosamente desde {file_path}")
    # Visualizar la nube de puntos
    o3d.visualization.draw_geometries(
        [point_cloud],
        window_name="Visualización de nube de puntos",
        width=800,  # Ancho de la ventana
        height=600,  # Alto de la ventana
        left=50,  # Posición horizontal de la ventana
        top=50   # Posición vertical de la ventana
    )
else:
    print(f"Error: No se pudo cargar la nube de puntos desde {file_path}")
