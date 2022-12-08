import logging

import matplotlib.pyplot as plt
from colorama import Fore
from skimage.filters import threshold_isodata
from masking import get_mask
from object_separation import BoundingBox
from object_separation import get_polygon_and_items


def check_image(path_to_image, with_images=False, threshold=threshold_isodata, threshold_delimeter=1.2,
                opening_radius=30):
    mask = get_mask(path_to_image, threshold=threshold, threshold_delimeter=threshold_delimeter,
                    opening_radius=opening_radius)

    if with_images:
        plt.imshow(plt.imread(path_to_image))
        plt.show()
        plt.imshow(mask, cmap='gray')
        plt.show()

    polygon, items = get_polygon_and_items(mask)

    if items and polygon:
        logging.info(f"Polygon: {polygon}\n items count: {len(items)}\n"
                     f"items: {items}")
        placer = Placer(polygon, items)
        if placer.is_get_in():
            logging.info(Fore.GREEN + "True")
            return True
        else:
            logging.info(Fore.RED + "False")
            return False

    if polygon:
        logging.info(Fore.GREEN + f"No items was found\nTrue")
        logging.info(Fore.GREEN + "True")
        return True
    else:
        logging.info(Fore.RED + f"No polygon was found\nFalse")
        logging.info(Fore.RED + "False")
        return False


class Placer:
    def __init__(self, polygon: BoundingBox, items: list[BoundingBox]):
        self.polygon = polygon
        self.items = items
        self.levels = list[Level]()
        self.levels_height = 0

    def is_get_in(self):
        if not self._check_squares():
            return False

        self._transform_all_to_towers()
        self.items.sort(key=lambda x: x.height, reverse=True)

        if not self._add_level(self.items[0]):
            return False

        for i in range(1, len(self.items)):
            # проходим по всем levels и ищем самый подходящий
            min_free_width = None
            best_fit_level = None
            for level in self.levels:
                free_width = level.get_fill_params(self.items[i])
                if free_width and (not min_free_width or free_width < min_free_width):
                    min_free_width = free_width
                    best_fit_level = level
            if best_fit_level:
                best_fit_level.fill(self.items[i])  # Тогда размещаем в этом уровне
            elif not self._add_level(self.items[i]):
                return False

        logging.info(f"Placer fill the polygon:\n"
                     f"Polygon size was {self.polygon.width} x {self.polygon.height}\n"
                     f"Filled {self.polygon.width} x {self.levels_height}")

        logging.debug(f"Levels count: {len(self.levels)}\n"
                      f"Levels: {self.levels}")

        return True

    def _check_squares(self):
        # Проверяем возможно ли размещение, сравнивая площади:
        sum_items_square = 0
        for item in self.items:
            sum_items_square += item.square

        if sum_items_square > self.polygon.square:
            logging.info(f"Items square bigger than polygon square. {sum_items_square} > {self.polygon.square}")
            return False

        return True

    def _add_level(self, item):
        free_width = self.polygon.width - item.width
        if free_width < 0:
            logging.info(
                f"Can't add new level after {len(self.levels)}. The item width was bigger than polygon width. "
                f"{item.width} > {self.polygon.width}")
            return False

        self.levels_height += item.height
        if self.levels_height > self.polygon.height:
            logging.info(
                f"Can't add new level after {len(self.levels)}. Height of polygon is too small. "
                f"{self.levels_height} > {self.polygon.height}")
            return False

        self.levels.append(Level(item.height, free_width))
        return True

    def _transform_all_to_towers(self):
        self.polygon.transform_to_tower()
        for item in self.items:
            item.transform_to_tower()


class Level:
    def __init__(self, height, free_width):
        self.height = height
        self.free_width = free_width

    def get_fill_params(self, item: BoundingBox):
        if self.height < item.height:
            # Height of every next item is bigger than all previous, so the height of level should be bigger
            logging.error("Height of level is smaller than height of item.")
            return None

        free_width = self.free_width - item.width
        if free_width >= 0:
            return free_width

        return None

    # Размещаем предмет в этом уровне
    def fill(self, item: BoundingBox):
        self.free_width -= item.width

    def __str__(self):
        return f"(h: {self.height} fw: {self.free_width})"

    def __repr__(self):
        return self.__str__()
