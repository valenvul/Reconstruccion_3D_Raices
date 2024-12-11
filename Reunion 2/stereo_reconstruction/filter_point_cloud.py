import numpy as np

def filter_point_cloud(point_cloud, colors, filter='budha'):
    if filter == 'budha':
        point_cloud, colors = mascara_budha(point_cloud, colors)
    if filter == 'raiz':
        point_cloud, colors = mascara_raiz(point_cloud, colors)
    if filter == 'raiz_9mm':
        point_cloud, colors = mascara_raiz_9mm(point_cloud, colors)
    return point_cloud, colors

def mascara_budha(point_cloud, colors):
    x_min, x_max = 0, 10000
    y_min, y_max = -500, -100
    z_min, z_max = -10000, 10

    mask = (
            (point_cloud[:, 0] >= x_min) & (point_cloud[:, 0] <= x_max) &
            (point_cloud[:, 1] >= y_min) & (point_cloud[:, 1] <= y_max) &
            (point_cloud[:, 2] >= z_min) & (point_cloud[:, 2] <= z_max)
    )

    # filtering points according to the mask
    point_cloud = point_cloud[mask]
    colors = colors[mask]

    return point_cloud, colors

def mascara_raiz(point_cloud, colors):
    x_min, x_max = 200, 400
    y_min, y_max = 100, 300
    z_min, z_max = -100, 30

    mask = (
            (point_cloud[:, 0] >= x_min) & (point_cloud[:, 0] <= x_max) &
            (point_cloud[:, 1] >= y_min) & (point_cloud[:, 1] <= y_max) &
            (point_cloud[:, 2] >= z_min) & (point_cloud[:, 2] <= z_max)
    )

    # filtering points according to the mask
    point_cloud = point_cloud[mask]
    colors = colors[mask]

    return point_cloud, colors

def mascara_raiz_9mm(point_cloud, colors):
    x_min, x_max = -50, 300
    y_min, y_max = -100, 0
    z_min, z_max = -500, 10

    mask = (
            (point_cloud[:, 0] >= x_min) & (point_cloud[:, 0] <= x_max) &
            (point_cloud[:, 1] >= y_min) & (point_cloud[:, 1] <= y_max) &
            (point_cloud[:, 2] >= z_min) & (point_cloud[:, 2] <= z_max)
    )

    # filtering points according to the mask
    point_cloud = point_cloud[mask]
    colors = colors[mask]

    return point_cloud, colors