import glob
import os
import pickle
from pathlib import Path

import cv2
import numpy as np
import calib
from cv_utils import apply_colormap
from disparity.method_cre_stereo import CREStereo
from disparity.method_opencv_bm import StereoSGBM
from disparity.methods import Config, Calibration, InputPair
from utils import numeric_sort

import open3d as o3d


def read_pickle(calib_file):
    with open(calib_file, "rb") as f:
        calib_results = pickle.loads(f.read())
    return calib_results


def draw_axis(image, intrinsics, extrinsics):
    K, dist_coeffs = intrinsics
    rv, tv = extrinsics

    axis_len_x = 9 * square_size_mm
    axis_len_y = 6 * square_size_mm
    axis_len_z = -6 * square_size_mm
    axis_points = np.array([[0, 0, 0],
                            [axis_len_x, 0, 0],
                            [0, axis_len_y, 0],
                            [0, 0, axis_len_z]], dtype=np.float32)

    # Project 3D points to the 2D image plane
    axis_points, _ = cv2.projectPoints(axis_points, rv, tv, K, dist_coeffs)

    # Draw the axes on the image
    axis_points = axis_points.reshape(-1, 2)
    origin = tuple(axis_points[0].ravel())

    #  show_image = cv2.undistort(img, left_cam_matrix, left_dist_coeffs)
    show_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    def draw_line(img, pt1, pt2, color, thickness=3):
        pt1 = (np.round(pt1[0]).astype(int), np.round(pt1[1]).astype(int))
        pt2 = (np.round(pt2[0]).astype(int), np.round(pt2[1]).astype(int))
        ret = cv2.line(img, pt1, pt2, color, thickness)
        return ret

    draw_line(show_image, origin, axis_points[1], (0, 0, 255), 10)
    draw_line(show_image, origin, axis_points[2], (0, 255, 0), 10)
    draw_line(show_image, origin, axis_points[3], (255, 0, 0), 10)

    # cv2.imshow("axis", show_image)
    # cv2.waitKey(0)
    return show_image


def undistort(maps, left_image, right_image):
    # Applying stereo image rectification on the left image
    left_rectified = cv2.remap(
        left_image,
        maps['left_map_x'],
        maps['left_map_y'],
        cv2.INTER_LINEAR,
        cv2.BORDER_CONSTANT,
        0
    )

    # Applying stereo image rectification on the right image
    right_rectified = cv2.remap(
        right_image,
        maps['left_map_x'],
        maps['left_map_y'],
        cv2.INTER_LINEAR,
        cv2.BORDER_CONSTANT,
        0
    )

    return left_rectified, right_rectified


def get_disparity_method(
        image_size,
        K,
        baseline_meters
):
    models_path = Path("data/models")
    config = Config(models_path=models_path)

    method = CREStereo(config)
    # method = StereoSGBM(config)

    w, h = image_size
    fx = K[0, 0]
    fy = K[1, 1]
    cx = K[0, 2]
    cy = K[1, 2]

    j_calib = {
        "width": w,
        "height": h,
        "baseline_meters": baseline_meters,
        "fx": fx,
        "fy": fy,
        "cx0": cx,
        "cx1": cx,
        "cy": cy,
        "depth_range": [0.1, 30.0],
        "left_image_rect_normalized": [0, 0, 1, 1]
    }

    calibration = Calibration(**j_calib)

    return method, calibration


def compute_disparity(
        disparity_method,
        left_image_rectified,
        right_image_rectified
):
    method, calibration = disparity_method
    pair = InputPair(left_image_rectified, right_image_rectified, calibration)
    disparity = method.compute_disparity(pair)

    return disparity.disparity_pixels


def pix(np_array):
    return tuple(np.round(np_array).astype(int))


def draw_correspondences(img_left, img_right, corners_left, corners_right):
    corners_left = np.float32(corners_left)
    corners_right = np.float32(corners_right)

    # Combinar ambas imágenes en una sola para dibujar las correspondencias
    combined_image = np.hstack((img_left, img_right))

    # Dibujar líneas entre las correspondencias de las dos imágenes
    for i in range(len(corners_left)):
        # Obtener las coordenadas de los puntos en ambas imágenes
        point_left = tuple(corners_left[i].ravel())
        point_right = tuple(corners_right[i].ravel() + np.array([img_left.shape[1], 0]))  # Desplazar en x

        point_left = pix(point_left)
        point_right = pix(point_right)

        # Dibujar el punto en ambas imágenes
        cv2.circle(combined_image, point_left, 5, (0, 255, 0), -1)
        cv2.circle(combined_image, point_right, 5, (0, 255, 0), -1)

        # Dibujar la línea que une los puntos correspondientes
        cv2.line(combined_image, point_left, point_right, (255, 0, 0), 1)

    return combined_image

def find_depth(
        corners_left,
        corners_right,
        left_K,
        baseline
):

    fx = left_K[0, 0]
    fy = left_K[1, 1]
    cx = left_K[0, 2]
    cy = left_K[1, 1]

    ret = []
    for left_corner, right_corner in zip(corners_left, corners_right):
        disp = np.linalg.norm(left_corner - right_corner)

        Z = fx * baseline / disp
        print(left_corner, right_corner, disp, Z)

        x, y = left_corner.ravel()
        X = (x - cx) * Z / fx
        Y = (y - cy) * Z / fx

        ret.append([X, Y, Z])

    ret = np.array(ret).reshape(-1, 3)
    return ret


if __name__ == "__main__":

    calib_file = "data/stereo/stereo_calibration.pkl"
    maps_file = "data/stereo/stereo_maps.pkl"

    input_dir = "data/stereo/captures/budha_board"
    left_files_pattern = "*left*.jpg"
    right_files_pattern = "*right*.jpg"

    checkerboard = (10, 7)
    square_size_mm = 24.2

    object_points = calib.board_points(checkerboard)
    object_points_mm = object_points * square_size_mm

    calibration = read_pickle(calib_file)
    maps = read_pickle(maps_file)

    left_K = calibration["left_K"]
    left_dist = calibration["left_dist"]
    right_K = calibration["right_K"]
    right_dist = calibration["right_dist"]
    image_size = calibration["image_size"]
    T = calibration["T"]

    left_map_x = maps["left_map_x"]
    left_map_y = maps["left_map_y"]
    right_map_x = maps["right_map_x"]
    right_map_y = maps["right_map_y"]
    P1 = maps["P1"]
    P2 = maps["P2"]
    Q = maps["Q"]

    # P2[0, 3] = 60

    baseline_mm = np.linalg.norm(T)

    method = get_disparity_method(
        image_size,
        P1,
        baseline_meters=baseline_mm / 1000
    )

    left_file_names = sorted(
        glob.glob(
            os.path.join(input_dir, left_files_pattern)
        ),
        key=numeric_sort
    )

    right_file_names = sorted(
        glob.glob(
            os.path.join(input_dir, right_files_pattern)
        ),
        key=numeric_sort
    )

    num_left = len(left_file_names)
    num_right = len(right_file_names)

    if num_left != num_right:
        raise Exception(f"the number of files (left {num_left} / right{num_right}) doesn't match")

    export_num = 0
    for left_file_name, right_file_name in zip(
            left_file_names, right_file_names
    ):

        print("processing", left_file_name, right_file_name)

        # read left and right images
        left_image = cv2.imread(left_file_name, cv2.IMREAD_GRAYSCALE)
        right_image = cv2.imread(right_file_name, cv2.IMREAD_GRAYSCALE)

        # get the images sizes
        left_size = (left_image.shape[1], left_image.shape[0])
        right_size = (right_image.shape[1], right_image.shape[0])

        # checks that images sizes match
        if left_size != right_size:
            raise Exception(f"left and right images sizes differ: left {left_size} / right {right_size}")

        if left_size != image_size:
            raise Exception(f"capture images sizes differ from calibration?: {left_size} / calib {image_size}")

        left_image_rectified = cv2.remap(left_image, left_map_x, left_map_y, cv2.INTER_LINEAR)
        right_image_rectified = cv2.remap(right_image, right_map_x, right_map_y, cv2.INTER_LINEAR)

        # pose
        left_found, left_corners = calib.detect_board(checkerboard, left_image_rectified)
        right_found, right_corners = calib.detect_board(checkerboard, right_image_rectified)

        left_color = cv2.cvtColor(left_image_rectified, cv2.COLOR_GRAY2BGR)
        right_color = cv2.cvtColor(right_image_rectified, cv2.COLOR_GRAY2BGR)
        # left_board_image = calib.draw_checkerboard(left_color, checkerboard, left_corners, left_found)
        # right_board_image = calib.draw_checkerboard(right_color, checkerboard, right_corners, right_found)
        # cv2.imshow("left board", left_board_image)
        # cv2.imshow("right board", right_board_image)
        # detection = np.hstack((left_board_image, right_board_image))
        corr = draw_correspondences(left_color, right_color, left_corners, right_corners)
        cv2.imshow("correspondences", corr)
        # cv2.imshow("checkerboard", detection)

        checkerboard_points_3d = find_depth(left_corners, right_corners, P1, baseline_mm)
        ch_w, ch_h = checkerboard
        corners_corners_3d = checkerboard_points_3d[[
            0,
            ch_w - 1,
            (ch_w * ch_h) - 1,
            ch_w * (ch_h - 1),
        ]]

        # Crear un LineSet vacío

        # Agregar los puntos al LineSet
        pt0 = checkerboard_points_3d[0]
        pt1 = checkerboard_points_3d[ch_w - 1]
        pt2 = checkerboard_points_3d[ch_w * (ch_h - 1)]

        # versors
        vx = pt1 - pt0
        vx /= np.linalg.norm(vx)
        vy = pt2 - pt0
        vy /= np.linalg.norm(vy)

        vz = np.cross(vx, vy)
        vz /= np.linalg.norm(vz)

        x_ori = pt0
        x_dst = pt0 + vx * square_size_mm * 9

        y_ori = pt0
        y_dst = pt0 + vy * square_size_mm * 6

        z_ori = pt0
        z_dst = pt0 + -vz * square_size_mm * 6

        red = [1.0, 0.0, 0.0]
        green = [0.0, 1.0, 0.0]
        blue = [0.0, 0.0, 1.0]

        ax_x = o3d.geometry.LineSet()
        ax_x.points = o3d.utility.Vector3dVector([x_ori, x_dst])
        ax_x.lines = o3d.utility.Vector2iVector([[0, 1]])
        ax_x.colors = o3d.utility.Vector3dVector(np.array([red]))

        ax_y = o3d.geometry.LineSet()
        ax_y.points = o3d.utility.Vector3dVector([y_ori, y_dst])
        ax_y.lines = o3d.utility.Vector2iVector([[0, 1]])
        ax_y.colors = o3d.utility.Vector3dVector(np.array([green]))

        ax_z = o3d.geometry.LineSet()
        ax_z.points = o3d.utility.Vector3dVector([z_ori, z_dst])
        ax_z.lines = o3d.utility.Vector2iVector([[0, 1]])
        ax_z.colors = o3d.utility.Vector3dVector(np.array([blue]))

        # Definir los vértices del rectángulo
        # vertices = np.array([x_ori, x_dst, y_dst, z_dst])
        #
        # # Crear los triángulos
        # triangles = np.array([[0, 1, 2], [0, 2, 3]])
        #
        # # Crear la malla
        # mesh = o3d.geometry.TriangleMesh()
        # mesh.vertices = o3d.utility.Vector3dVector(vertices)
        # mesh.triangles = o3d.utility.Vector3iVector(triangles)

        box_z = square_size_mm * 16
        box_x = square_size_mm * 16
        box_y = square_size_mm * 9

        t_ini = pt0 - vx * square_size_mm * 3 - vy * square_size_mm * 8.5 + vz * square_size_mm * 2
        t_end = t_ini + vx * box_x + -vz * box_z
        t_center = (t_ini + t_end) / 2
        # v0 = t_ini
        # v1 = t_ini + vx * box_x
        # v2 = t_ini - vz * box_z
        # v3 = t_ini + vx * box_x + -vz * box_z
        #
        #
        # mesh = o3d.geometry.TriangleMesh()
        # mesh.vertices = o3d.utility.Vector3dVector([v0, v1, v2, v3])
        # #mesh.vertices = o3d.utility.Vector3dVector([v1, v2, v3])
        #
        # mesh.triangles = o3d.utility.Vector3iVector([
        #     [0, 1, 2], [1, 0, 2],
        #     [1, 2, 3], [2, 1, 3],
        #     # [1, 2, 3],
        # ])
        #
        # red = [1.0, 0.0, 0.0]
        # colors = np.array([red, red, red, red])
        # mesh.vertex_colors = o3d.utility.Vector3dVector(colors)

        # Definir los colores con transparencia (50% de transparencia)
        # colors = np.array([[1, 0, 0, 0.5], [1, 0, 0, 0.5], [1, 0, 0, 0.5], [1, 0, 0, 0.5]])
        # mesh.vertex_colors = o3d.utility.Vector3dVector(colors)

        # Crear una matriz de rotación a partir de las direcciones
        R = np.column_stack((vx, vy, -vz))

        # Crear la caja orientada con el vértice y las dimensiones
        box = o3d.geometry.OrientedBoundingBox(center=t_center, R=R, extent=[box_x, box_y, box_z])


        cv2.waitKey()

        # ESTO NO ANDA Y NO SE BIEN POR QUE
        # points_4D_homogeneous = cv2.triangulatePoints(P1, P2, left_corners.T, right_corners.T)
        # points_4D_homogeneous = points_4D_homogeneous.reshape(-1, 4)
        # convierte de coordenadas homogéneas a euclidianas (dividiendo por w)
        # points_3D = points_4D_homogeneous[:3] / points_4D_homogeneous[3]
        # Transponer para tener los puntos en forma (N, 3)
        # points_3D = points_3D.T

        checkerboard_pcd = o3d.geometry.PointCloud()
        checkerboard_pcd.points = o3d.utility.Vector3dVector(
             corners_corners_3d.reshape(-1, corners_corners_3d.shape[-1])
        )

        ret, rvec, tvec = cv2.solvePnP(
            object_points_mm,
            left_corners,
            left_K,
            left_dist
        )

        axis_image = draw_axis(
            left_image,
            (left_K, left_dist),
            (rvec, tvec)
        )

        # disparity

        # object_points_mm = np.array(object_points_mm, dtype=np.float32)
        # image_points = np.array(corners, dtype=np.float32)

        disparity = compute_disparity(
            method,
            left_image_rectified,
            right_image_rectified
        )

        points_3d = cv2.reprojectImageTo3D(disparity, Q)

        point_cloud = points_3d.reshape(-1, points_3d.shape[-1])
        good_points = ~np.isinf(point_cloud).any(axis=1)

        colors = cv2.cvtColor(left_image_rectified, cv2.COLOR_BGR2RGB).astype(np.float64) / 255.0
        colors = colors.reshape(-1, points_3d.shape[-1])

        point_cloud = point_cloud[good_points]
        colors = colors[good_points]

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(point_cloud)
        pcd.colors = o3d.utility.Vector3dVector(colors)

        # Filtrar los puntos que están dentro de la caja
        indices_in_box = box.get_point_indices_within_bounding_box(pcd.points)

        # Obtener los puntos filtrados
        pcd = pcd.select_by_index(indices_in_box)

        pcd, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
        # pcd, _ = pcd.remove_radius_outlier(nb_points=16, radius=0.05)

        o3d.io.write_point_cloud(f"data/results/output_{export_num}.pcd", pcd)
        export_num += 1

        o3d.visualization.draw_geometries([
            pcd, checkerboard_pcd, ax_x, ax_y, ax_z, box
        ])

        #pcd.colors = o3d.utility.Vector3dVector(colors / 255.0)

        # filtered_pcd = pcd
        # Visualizar la nube de puntos filtrada
        o3d.visualization.draw_geometries([pcd])

        disp_vis = disparity.copy()
        disp_vis = 255 * (disp_vis - disp_vis.min()) / (disp_vis.max() - disp_vis.min())
        disp_vis = disp_vis.astype('uint8')
        disp_vis = apply_colormap(disp_vis)

        cv2.imshow("axis", axis_image)
        cv2.imshow("disparity", disp_vis)
        cv2.waitKey(0)
