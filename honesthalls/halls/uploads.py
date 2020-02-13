import os
from django.conf import settings
from PIL import Image
from math import ceil, floor


def process_uploaded_image(filename):
    im = Image.open(filename)
    im = scale_and_crop_image(im, settings.MEDIA_IMAGE_MAX_SIZE,
                              settings.MEDIA_IMAGE_ASPECT_RATIO)
    im.save(filename, 'JPEG', quality=90)


def remove_unused_image(filename):
    os.remove(filename)


def scale_and_crop_image(im, max_dim, aspect_ratio):
    # Fix aspect ratio
    width, height = im.size
    exp_width, exp_height = width, height
    aspect = width / height

    if aspect >= aspect_ratio:
        # Wider than it should be
        exp_width = height * aspect_ratio
    else:
        # Taller than it should be
        exp_height = width / aspect_ratio

    # Calculate how much to crop
    crop_x = (width - exp_width) / 2
    crop_y = (height - exp_height) / 2

    # Crop the image
    im = im.crop((ceil(crop_x), ceil(crop_y),
                  width - floor(crop_x), height - floor(crop_y)))

    # thumbnail() works in-place
    im.thumbnail((max_dim, max_dim), Image.NEAREST)
    return im
