import logging
from skimage.measure import find_contours
import numpy as np

MAX_POLYGON_LINE_WIDTH = 40


def get_polygon_and_items(mask):
    """ Многоугольник - объект с самой большой координатой по x на изображении.
    При выделении контуров многоугольника выделяется 2 контура, внешний и внутренний.
    Нам нужен внутренний контур.

    :return tuple of bboxes (polygon, [items])
    """
    contours = find_contours(mask)
    boxes = [BoundingBox(contour) for contour in contours]
    inside = boxes[0]
    outside = None
    for box in boxes:
        if box.x_min > inside.x_min:
            outside = inside
            inside = box

    if outside is None or inside.x_min - outside.x_min > MAX_POLYGON_LINE_WIDTH:
        logging.error(f"Can't find polygon. \n"
                      f"outside: {outside}"
                      f"inside: {inside}"
                      f"all boxes: {boxes}")
        return None, None

    boxes.remove(inside)
    boxes.remove(outside)

    return inside, boxes


class BoundingBox:
    def __init__(self, contour):
        self.x_min, self.x_max, self.y_min, self.y_max = self.to_bbox_tuple(contour)
        self.width = self.x_max - self.x_min
        self.height = self.y_max - self.y_min
        self.square = self.width * self.height

    def transform_to_tower(self):
        if self.width > self.height:
            tmp = self.height
            self.height = self.width
            self.width = tmp

    def __str__(self):
        return f"(h: {self.height} w: {self.width})"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def to_bbox_tuple(contour):
        x_min = np.min(contour[:, 1])
        x_max = np.max(contour[:, 1])
        y_min = np.min(contour[:, 0])
        y_max = np.max(contour[:, 0])
        return x_min, x_max, y_min, y_max
