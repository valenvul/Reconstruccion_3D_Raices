import glob
import os
import cv2
import pickle
import calib
from utils import numeric_sort, np_print


def calibrate(
        calib_images_directory,
        checkerboard,
        square_size,
        output_file,
):
    checkerboard = checkerboard
    checkerboard_world_points_mm = square_size * calib.board_points(checkerboard)

    files_pattern = "*.jpg"

    file_names = sorted(
        glob.glob(
            os.path.join(calib_images_directory, files_pattern)
        ),
        key=numeric_sort
    )


    num_images = len(file_names)

    image_size = None

    images_points = []
    world_points_mm = []

    for file_name in file_names:

        print("processing", file_name)

        # images
        image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

        # get the images sizes
        size = (image.shape[1], image.shape[0])

        if image_size is None:
            # remembers the images size
            image_size = size
        else:
            if image_size != size:
                raise Exception(f"there are images with different sizes: {image_size} vs {size}")

        # finds the checkerboard in each image
        found, corners = calib.detect_board(checkerboard, image)

        if not found:
            print("warning, checkerboard was not found")
            continue

        images_points.append(corners)
        world_points_mm.append(checkerboard_world_points_mm)

    if len(images_points) < 10:
        print("not enough images found. can't calibrate")

    world_points_mm = [p.reshape(-1, 3) for p in world_points_mm]
    images_points = [p.reshape(-1, 2) for p in images_points]

    ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
        world_points_mm,
        images_points,
        image_size, None, None
    )

    to_print = [

        "# Camera Intrinsics:",
        ("K", K),
        ("dist", dist),


    ]
    print("# CALIBRATION")
    for line in to_print:

        if isinstance(line, str):
            print(line)
        else:
            var_name, np_array = line
            print(f"{var_name} = {np_print(np_array)}\n")

    calibration_results = {
        'K': K,
        'dist': dist,
        "image_size": image_size
    }

    with open(output_file, "wb") as f:
        f.write(pickle.dumps(calibration_results))

    return calibration_results

def create_rectifying_maps(
    calibration_results,
    output_file,
):

    K = calibration_results['K']
    dist = calibration_results['dist']
    image_size = calibration_results['image_size']

    alpha = 0
    new_K, roi = cv2.getOptimalNewCameraMatrix(K, dist, image_size, alpha, image_size)

    print("creating undistortion maps...")
    map_x, map_y = cv2.initUndistortRectifyMap(K, dist, None, new_K, image_size, cv2.CV_32FC1)

    maps = {

        # undistorting maps
        "map_x": map_x,
        "map_y": map_y,

        "image_size": image_size

    }

    with open(output_file, "wb") as f:
        f.write(pickle.dumps(maps))

    return maps


def do_calibration(
        checkerboard,
        square_size,
        calib_images_dir,
        calib_results_dir
):
    calib_file = os.path.join(calib_results_dir, "mono_calibration.pkl")
    undistort_maps_file = os.path.join(calib_results_dir, "mono_maps.pkl")

    print("calibrating...")
    if os.path.exists(
            calib_file
    ):
        with open(calib_file, "rb") as f:
            calib_results = pickle.loads(f.read())
    else:
        calib_results = calibrate(
            calib_images_dir,
            checkerboard,
            square_size,
            calib_file
        )

    print("computing undistortion maps...")
    if os.path.exists(
            undistort_maps_file
    ):
        with open(undistort_maps_file, "rb") as f:
            maps = pickle.loads(f.read())
    else:
        maps = create_rectifying_maps(
            calib_results,
            undistort_maps_file
        )

    return calib_results, maps


def undistort(calib_results, maps, input_dir, output_dir):

    image_size = calib_results['image_size']
    map_x = maps['map_x']
    map_y = maps['map_y']

    files_pattern = "*.jpg"


    file_names = sorted(
        glob.glob(
            os.path.join(input_dir, files_pattern)
        ),
        key=numeric_sort
    )

    for file_name in file_names:

        print("processing", file_name)

        # read image
        image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

        # get the images sizes
        size = (image.shape[1], image.shape[0])

        if size != image_size:
            raise Exception(f"capture images sizes differ from calibration?: {size} / calib {image_size}")

        image_rectified = cv2.remap(image, map_x, map_y, cv2.INTER_LINEAR)

        rfile_name = "rect_" + os.path.split(file_name)[1]
        output_file = os.path.join(output_dir, rfile_name)

        print(f"writting undistorted image {rfile_name}...")
        cv2.imwrite(output_file, image_rectified)



if __name__ == "__main__":
    # calibration parameters
    calib_images_dir = "data/mono/calib"
    calib_results_dir = "data/mono"
    checkerboard = (10, 7)
    square_size = 24.2

    # captures
    #captures_dir = "data/mono/captures/budha_board"
    #rectified_dir = "data/mono/captures/rect_budha_board"

    captures_dir = "data/mono/captures/budha_sfm"
    rectified_dir = "data/mono/captures/rect_budha_sfm"

    calib_results, maps = do_calibration(
        checkerboard=checkerboard,
        square_size=square_size,
        calib_images_dir=calib_images_dir,
        calib_results_dir=calib_results_dir
    )

    undistort(
        calib_results,
        maps,
        captures_dir,
        rectified_dir
    )
