import glob
import os
import cv2
import pickle
import calib
from utils import numeric_sort, np_print


def calibrate_stereo(
        calib_images_directory,
        checkerboard,
        square_size,
        output_file,
):
    checkerboard = checkerboard
    # calib.board_points(checkerboard) devuelve un conjunto de triplas con las coordenadas de todas las esquinas del tablero en el mundo de la imagen
    # multiplicando por el tamaño de los cuadrados se las lleva a coordenadas con tamaño del mundo rea
    checkerboard_world_points_mm = square_size * calib.board_points(checkerboard)

    # Separa las imagenes izquierdas de las derechas
    left_files_pattern = "*left*.jpg"
    right_files_pattern = "*right*.jpg"

    # Las ordena segun el numero
    left_file_names = sorted(
        glob.glob(
            os.path.join(calib_images_directory, left_files_pattern)
        ),
        key=numeric_sort
    )

    right_file_names = sorted(
        glob.glob(
            os.path.join(calib_images_directory, right_files_pattern)
        ),
        key=numeric_sort
    )

    # se asegura que haya la misma cantidad de imágenes izquierda y derecha
    num_left = len(left_file_names)
    num_right = len(right_file_names)

    if num_left != num_right:
        raise Exception(f"the number of files (left {num_left} / right{num_right}) doesn't match")
    image_size = None

    left_images_points = []
    right_images_points = []
    world_points_mm = []

    for left_file_name, right_file_name in zip(
            left_file_names, right_file_names
    ):

        print("processing", left_file_name, right_file_name)

        # read left and right images
        # Se leen en blanco y negro para usar calib.detect_board
        left_image = cv2.imread(left_file_name, cv2.IMREAD_GRAYSCALE)
        right_image = cv2.imread(right_file_name, cv2.IMREAD_GRAYSCALE)

        # get the images sizes
        left_size = (left_image.shape[1], left_image.shape[0])
        right_size = (right_image.shape[1], right_image.shape[0])

        # checks that images sizes match
        if left_size != right_size:
            raise Exception(f"left and right images sizes differ: left {left_size} / right {right_size}")

        if image_size is None:
            # remembers the images size
            image_size = left_size
        else:
            if image_size != left_size:
                raise Exception(f"there are images with different sizes: {image_size} vs {left_size}")


        # calib.detect_board(checkerboard, image)
        # finds the checkerboard in each image
        left_found, left_corners = calib.detect_board(checkerboard, left_image)
        right_found, right_corners = calib.detect_board(checkerboard, right_image)

        if not left_found or not right_found:
            print("warning, checkerboard was not found")
            continue

        left_images_points.append(left_corners)
        right_images_points.append(right_corners)
        world_points_mm.append(checkerboard_world_points_mm)

    if len(left_images_points) < 10:
        print("not enough images found. can't calibrate")

    world_points_mm = [p.reshape(-1, 3) for p in world_points_mm]
    left_images_points = [p.reshape(-1, 2) for p in left_images_points]
    right_images_points = [p.reshape(-1, 2) for p in right_images_points]

    # left_K, left_dist = left_calibration[0], left_calibration[1]
    # right_K, right_dist = right_calibration[0], right_calibration[1]
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
        # 'left_pts': left_pts,
        # 'right_pts': right_pts
    }

    with open(output_file, "wb") as f:
        f.write(pickle.dumps(calibration_results))

    return calibration_results


def create_stereo_rectifying_maps(
        calibration_results,
        output_file,
):
    left_K = calibration_results['left_K']
    left_dist = calibration_results['left_dist']
    right_K = calibration_results['right_K']
    right_dist = calibration_results['right_dist']
    image_size = calibration_results['image_size']
    R = calibration_results['R']
    T = calibration_results['T']

    print("rectifying stereo...")
    R1, R2, P1, P2, Q, validRoi1, validRoi2 = cv2.stereoRectify(
        left_K, left_dist, right_K, right_dist, image_size, R, T, alpha=0
    )

    print("creating undistortion maps...")
    left_map_x, left_map_y = cv2.initUndistortRectifyMap(left_K, left_dist, R1, P1, image_size, cv2.CV_32FC1)
    right_map_x, right_map_y = cv2.initUndistortRectifyMap(right_K, right_dist, R2, P2, image_size, cv2.CV_32FC1)

    stereo_maps = {

        # undistorting maps
        "left_map_x": left_map_x,
        "left_map_y": left_map_y,
        "right_map_x": right_map_x,
        "right_map_y": right_map_y,

        # add also rectifying info:
        "R1": R1,
        "R2": R2,
        "P1": P1,
        "P2": P2,
        "Q": Q,
        "validRoi1": validRoi1,
        "validRoi2": validRoi2,

    }

    with open(output_file, "wb") as f:
        f.write(pickle.dumps(stereo_maps))

    return stereo_maps


def do_calibration(
        checkerboard,
        square_size,
        calib_images_dir,
        calib_results_dir
):
    # busco los archivos donde voy a guardar los resultados
    calib_stereo_file = os.path.join(calib_results_dir, "stereo_calibration.pkl")
    undistort_maps_file = os.path.join(calib_results_dir, "stereo_maps.pkl")

    print("calibrating stereo...")
    # si el archivo ya exitse ya esta hecha la calibración y la lee
    if os.path.exists(
            calib_stereo_file
    ):
        with open(calib_stereo_file, "rb") as f:
            calib_results = pickle.loads(f.read())
    else:
        # Sino calibra en base a las imágenes
        #calibrate_stereo(calib_images_directory, checkerboard, square_size, output_file,) definido en este archivo
        calib_results = calibrate_stereo(
            calib_images_dir,
            checkerboard,
            square_size,
            calib_stereo_file
        )

    print("computing undistortion maps...")
    # si los mapas de desdistorision ya existen los lee
    if os.path.exists(
            undistort_maps_file
    ):
        with open(undistort_maps_file, "rb") as f:
            maps = pickle.loads(f.read())
    else:
        #sino los calcula
        # create_stereo_rectifying_maps(calibration_results, output_file,) definido en este archivo
        maps = create_stereo_rectifying_maps(
            calib_results,
            undistort_maps_file
        )

    return calib_results, maps


def undistort(calib_results, maps, input_dir, output_dir):

    image_size = calib_results['image_size']
    left_map_x = maps['left_map_x']
    left_map_y = maps['left_map_y']
    right_map_x = maps['right_map_x']
    right_map_y = maps['right_map_y']

    left_files_pattern = "*left*.jpg"
    right_files_pattern = "*right*.jpg"

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

        rleft_file_name = "rect_" + os.path.split(left_file_name)[1]
        rright_file_name = "rect_" + os.path.split(right_file_name)[1]
        output_left_file = os.path.join(output_dir, rleft_file_name)
        output_right_file = os.path.join(output_dir, rright_file_name)

        print(f"writting undistorted images {rleft_file_name}, {rright_file_name}...")
        cv2.imwrite(output_left_file, left_image_rectified)
        cv2.imwrite(output_right_file, right_image_rectified)


# Acá se llama a las funciones para la calibración de la cámara
if __name__ == "__main__":
    # calibration parameters
    calib_images_dir = "data/stereo/calib"
    calib_results_dir = "data/stereo"
    checkerboard = (10, 7)
    square_size = 24.2

    # captures
    #captures_dir = "data/stereo/captures/budha_board"
    #rectified_dir = "data/stereo/captures/rect_budha_board"

    captures_dir = "data/stereo/captures/budha_vo"
    rectified_dir = "data/stereo/captures/rect_budha_vo"

    #do_calibration(checkerboard, square_size, calib_images_dir, calib_results_dir) definido en este archivo
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
