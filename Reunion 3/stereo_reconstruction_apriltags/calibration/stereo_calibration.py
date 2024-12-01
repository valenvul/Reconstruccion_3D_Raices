import pickle
import os

from calibration.rectifying_maps import create_stereo_rectifying_maps
from calibration.camera_calibration import calibrate_stereo


def do_calibration(
        checkerboard,
        square_size,
        calib_images_dir,
        calib_results_dir
):
    # files for calibration results
    calib_stereo_file = os.path.join(calib_results_dir, "stereo_calibration.pkl")
    undistort_maps_file = os.path.join(calib_results_dir, "stereo_maps.pkl")

    # first we compute the calibration parameters
    print("calibrating stereo...")
    # if the calibration exists read the results
    if os.path.exists(
            calib_stereo_file
    ):
        with open(calib_stereo_file, "rb") as f:
            calib_results = pickle.loads(f.read())
    else:
        # if not, calibrate based on calibration images
        calib_results = calibrate_stereo(
            calib_images_dir,
            checkerboard,
            square_size,
            calib_stereo_file
        )

    # then we compute the undistortion maps
    print("computing undistortion maps...")
    # if undistortion maps already exist read them
    if os.path.exists(
            undistort_maps_file
    ):
        with open(undistort_maps_file, "rb") as f:
            maps = pickle.loads(f.read())
    else:
        # if not, calculate them
        maps = create_stereo_rectifying_maps(
            calib_results,
            undistort_maps_file
        )

    return calib_results, maps