from pathlib import Path

from disparity.methods import Config, Calibration, InputPair
from disparity.method_cre_stereo import CREStereo


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

    # focal length and camera center
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

    # Reads json as calibration object
    calibration = Calibration(**j_calib)

    return method, calibration

def compute_disparity(
        disparity_method,
        left_image_rectified,
        right_image_rectified
):
    method, calibration = disparity_method
    pair = InputPair(left_image_rectified, right_image_rectified, calibration)
    # disparity algorithm from the disparity method defined before
    disparity = method.compute_disparity(pair)

    return disparity.disparity_pixels