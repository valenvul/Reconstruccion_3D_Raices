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

    # width an height
    w, h = image_size
    
    # foco y centro optico
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

    # Lee el json como un objeto de la clase Calibration de methods.py
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
    ## Una vez que se tienen calibradas las cámaras

    # defino los archivos en los que se tienen los parametros de calibracion y los remapeos de rectificacion
    calib_file = "data/stereo/stereo_calibration.pkl"
    maps_file = "data/stereo/stereo_maps.pkl"

    input_dir = "data/stereo/captures/budha_board"
    left_files_pattern = "*left*.jpg"
    right_files_pattern = "*right*.jpg"

    # Defino el objeto conocido entre las imágenes
    checkerboard = (10, 7)
    square_size_mm = 24.2

    # Detecto los puntos del objeto conocido y los paso a milimetros
    object_points = calib.board_points(checkerboard)
    object_points_mm = object_points * square_size_mm

    # leo los parametros y mapeos
    calibration = read_pickle(calib_file)
    maps = read_pickle(maps_file)

    # Rescato los atributos por separado
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

    #get_disparity_method(image_size, K, baseline_meters) definido en este archivo
    # Devuelve el metodo de calculo de disparidad y un objeto Calibration con los parametros de calibracion de la cámara
    method = get_disparity_method(
        image_size,
        P1,
        baseline_meters=baseline_mm / 1000
    )

    # Ordena los archivos
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

    all_points_3d = np.empty((0, 3))
    all_colors = np.empty((0, 3))
    all_camera_extrinsics = []
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

        # rectifica las imagenes
        left_image_rectified = cv2.remap(left_image, left_map_x, left_map_y, cv2.INTER_LINEAR)
        right_image_rectified = cv2.remap(right_image, right_map_x, right_map_y, cv2.INTER_LINEAR)

        # pose
        # se hace toda la deteccion sobre imagenes ya rectificadas. Tener en cuenta.
        left_found, left_corners = calib.detect_board(checkerboard, left_image_rectified)
        right_found, right_corners = calib.detect_board(checkerboard, right_image_rectified)

        left_color = cv2.cvtColor(left_image_rectified, cv2.COLOR_GRAY2BGR)
        right_color = cv2.cvtColor(right_image_rectified, cv2.COLOR_GRAY2BGR)
        # left_board_image = calib.draw_checkerboard(left_color, checkerboard, left_corners, left_found)
        # right_board_image = calib.draw_checkerboard(right_color, checkerboard, right_corners, right_found)
        # cv2.imshow("left board", left_board_image)
        # cv2.imshow("right board", right_board_image)
        # detection = np.hstack((left_board_image, right_board_image))
        # corr = draw_correspondences(left_color, right_color, left_corners, right_corners)
        #cv2.imshow("correspondences", corr)
        #cv2.waitKey(1)
        # cv2.imshow("checkerboard", detection)


        object_points = calib.board_points(checkerboard)
        object_points_mm = object_points * square_size_mm
        # rvec rota puntos del sistema de coordenadas del objeto al sistema de coordenadas de la cámara
        # solvePnP devuelve la rotacion y las traslacion de las camaras
        ret, rvec, tvec = cv2.solvePnP(
            object_points_mm,
            left_corners,
            left_K,
            left_dist,
            flags=cv2.SOLVEPNP_IPPE
        )

        # Armamos la matriz de transformación homogénea que convierte puntos del sistema de coordenadas del objeto a la cámara y vice versa
        c_R_o = cv2.Rodrigues(rvec)
        c_T_o = np.column_stack((c_R_o[0], tvec))
        c_T_o = np.vstack((c_T_o, [0, 0, 0, 1])) # T 4x4 que transforma puntos c_x = c_T_o  * o_x (en coordenadas del objeto a coodenadas de la cámara)
        o_T_c = np.linalg.inv(c_T_o) # T 4x4 que transforma puntos o_x = o_T_c  * c_x (en coordenadas de la camara a coodenadas del objeto)

        print(o_T_c)

        # disparity map
        disparity = compute_disparity(
            method,
            left_image_rectified,
            right_image_rectified
        )

        # Reproyecta los puntos al sistema de coordenadas 3D
        points_3d = cv2.reprojectImageTo3D(disparity, Q)

        point_cloud = points_3d.reshape(-1, points_3d.shape[-1])
        good_points = ~np.isinf(point_cloud).any(axis=1)

        colors = cv2.cvtColor(left_image_rectified, cv2.COLOR_BGR2RGB).astype(np.float64) / 255.0
        colors = colors.reshape(-1, points_3d.shape[-1])

        point_cloud = point_cloud[good_points]
        colors = colors[good_points]

        point_cloud = o_T_c @ np.vstack((point_cloud.T, np.ones(point_cloud.shape[0])))
        point_cloud = point_cloud[:3].T

        all_points_3d = np.row_stack((all_points_3d, point_cloud))
        all_colors = np.row_stack((all_colors, colors))
        all_camera_extrinsics.append(c_T_o)

    # Eje de coordenadas del mundo (debería coincidir con la esquina del patron)
    axis = o3d.geometry.TriangleMesh.create_coordinate_frame(size=300.0, origin=[0, 0, 0])

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(all_points_3d)
    pcd.colors = o3d.utility.Vector3dVector(all_colors)

    print(left_K.dtype)
    print(o_T_c.dtype)
    camera_frustums = []
    for c_T_o in all_camera_extrinsics:
        camera_frustum = o3d.geometry.LineSet.create_camera_visualization(view_width_px=left_size[1], view_height_px=left_size[0], intrinsic=left_K[:3, :3],
                                                                            extrinsic=c_T_o)
        camera_frustum.scale(100, camera_frustum.get_center())
        camera_frustums.append(camera_frustum)

    o3d.visualization.draw_geometries([pcd, axis, *camera_frustums])