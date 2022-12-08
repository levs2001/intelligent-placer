import os

_DATASET_TRUE = "./dataset/true/"
_DATASET_FALSE = "./dataset/false/"

_true_images = [_DATASET_TRUE + img for img in os.listdir(_DATASET_TRUE) if
                os.path.isfile(_DATASET_TRUE + img) and img.lower().endswith(".jpg")]
_true_images.sort()

_false_images = [_DATASET_FALSE + img for img in os.listdir(_DATASET_FALSE) if
                 os.path.isfile(_DATASET_FALSE + img) and img.lower().endswith(".jpg")]
_false_images.sort()


def get_true_images():
    return _true_images


def get_true_image(num):
    return _true_images[num]


def get_false_images():
    return _false_images


def get_false_image(num):
    return _false_images[num]
