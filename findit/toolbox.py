import cv2
import numpy as np
import imutils
import typing
import copy
import datetime


class Point(object):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def to_tuple(self) -> tuple:
        return self.x, self.y


def load_grey_from_path(pic_path: str) -> np.ndarray:
    """ load grey picture (with cv2) from path """
    raw_img = cv2.imread(pic_path)
    return load_grey_from_cv2_object(raw_img)


def load_grey_from_cv2_object(pic_object: np.ndarray) -> np.ndarray:
    """ preparation for cv2 object (force turn it into gray) """
    pic_object = pic_object.astype(np.uint8)
    try:
        # try to turn it into grey
        grey_pic = cv2.cvtColor(pic_object, cv2.COLOR_BGR2GRAY)
    except cv2.error:
        # already grey
        return pic_object
    return grey_pic


def pre_pic(pic_path: str = None, pic_object: np.ndarray = None) -> np.ndarray:
    """ this method will turn pic path and pic object into grey pic object """
    if pic_object is not None:
        return load_grey_from_cv2_object(pic_object)
    return load_grey_from_path(pic_path)


def resize_pic_scale(pic_object: np.ndarray, target_scale: np.ndarray) -> np.ndarray:
    return imutils.resize(pic_object, width=int(pic_object.shape[1] * target_scale))


def fix_location(pic_object: np.ndarray, location: typing.Sequence):
    """ location from cv2 should be left-top location, and need to fix it and make it central """
    # TODO not always works because of scale!
    size_x, size_y = pic_object.shape
    old_x, old_y = location
    return old_x + size_x / 2, old_y + size_y / 2


def mark_point(pic_object: np.ndarray,
               location: typing.Sequence,
               cover: bool = None) -> np.ndarray:
    """ draw a mark on your picture, or your picture copy. """
    if not cover:
        pic_object = copy.deepcopy(pic_object)
    distance = 50
    target_x, target_y = map(int, location)
    start_point = (target_x - distance, target_y - distance)
    end_point = (target_x + distance, target_y + distance)
    cv2.rectangle(pic_object, start_point, end_point, -1)
    return pic_object


def get_timestamp() -> str:
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')
