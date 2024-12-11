import cv2
import pickle


def create_stereo_rectifying_maps(
        calibration_results,
        output_file,
):
    # read calibration results
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