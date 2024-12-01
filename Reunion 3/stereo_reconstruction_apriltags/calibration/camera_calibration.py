import cv2
import pickle

from calibration.calib import board_points, detect_board
from utils import np_print
from images import *

def print_calib_results(E, F, R, T, left_K, left_dist, right_K, right_dist):
    to_print = [

        "# Left camera Intrinsics:",
        ("left_K", left_K),
        ("left_dist", left_dist),

        "# Right camera Intrinsics:",
        ("right_K", right_K),
        ("right_dist", right_dist),

        "# Rotation:",
        ("R", R),

        "# Translation:",
        ("T", T),

        "# Essential Matrix:",
        ("E", E),

        "# Fundamental Matrix:",
        ("F", F),

    ]
    print("# STEREO CALIBRATION")
    for line in to_print:

        if isinstance(line, str):
            print(line)
        else:
            var_name, np_array = line
            print(f"{var_name} = {np_print(np_array)}\n")

def calibrate_stereo(
        calib_images_directory,
        checkerboard,
        square_size,
        output_file,
):
    checkerboard_world_points_mm = square_size * board_points(checkerboard)

    left_file_names, right_file_names = prepare_imgs(calib_images_directory)

    # used to check correct image sizes
    image_size = None

    # arrays to store calibration points
    left_images_points = []
    right_images_points = []
    world_points_mm = []

    for left_file_name, right_file_name in zip(
            left_file_names, right_file_names
    ):

        image_size, left_image, right_image = process_images(left_file_name, right_file_name, image_size)

        # finds the checkerboard in each image
        left_found, left_corners = detect_board(checkerboard, left_image)
        right_found, right_corners = detect_board(checkerboard, right_image)

        if not left_found or not right_found:
            print("warning, checkerboard was not found")
            continue

        left_images_points.append(left_corners)
        right_images_points.append(right_corners)
        world_points_mm.append(checkerboard_world_points_mm)

    if len(left_images_points) < 10:
        print("not enough images found. can't calibrate")

    # reformat the arrays so world points is made of trios and images point of pairs
    world_points_mm = [p.reshape(-1, 3) for p in world_points_mm]
    left_images_points = [p.reshape(-1, 2) for p in left_images_points]
    right_images_points = [p.reshape(-1, 2) for p in right_images_points]

    left_K, left_dist = None, None
    right_K, right_dist = None, None

    err, left_K, left_dist, right_K, right_dist, R, T, E, F = cv2.stereoCalibrate(
        world_points_mm,
        left_images_points,
        right_images_points,
        left_K,
        left_dist,
        right_K,
        right_dist,
        image_size,
        flags=0
    )

    print_calib_results(E, F, R, T, left_K, left_dist, right_K, right_dist)

    calibration_results = {
        'left_K': left_K,
        'left_dist': left_dist,
        'right_K': right_K,
        'right_dist': right_dist,
        'R': R,
        'T': T,
        'E': E,
        'F': F,
        'image_size': image_size,
    }

    with open(output_file, "wb") as f:
        f.write(pickle.dumps(calibration_results))

    return calibration_results