import os
from django.conf import settings
from PIL import Image
from math import ceil, floor


def process_uploaded_image(filename):
    """
    Processes a file uploaded by the user.
    Overwrites the existing file.
    """
    im = Image.open(filename)
    # Crop the image to get desired aspect ratio
    im = change_image_aspect_ratio(im, settings.MEDIA_IMAGE_ASPECT_RATIO)
    # MEDIA_IMAGE_MAX_SIZE must be a float (eg. 1.33 for 4:3)
    max_size = settings.MEDIA_IMAGE_MAX_SIZE
    # thumbnail() works in-place
    im.thumbnail((max_size, max_size), Image.NEAREST)
    # Overwrite the input image file.
    im.save(filename, 'JPEG', quality=settings.MEDIA_IMAGE_QUALITY)


def remove_unused_image(filename):
    """ Handles the deletion of unused image files. """
    os.remove(filename)


def change_image_aspect_ratio(im, aspect_ratio):
    """
    Crops an image file to conform to a specified aspect ratio.
    The cropping is always centered.
    A new image is returned.
    """
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

    return im
