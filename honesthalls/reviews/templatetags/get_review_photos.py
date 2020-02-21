# THIS IS THE FUNCTION TO GET THE REVIEW PHOTOS
from django import template
from django.db import models
from halls.models import ReviewPhotos

register=template.Library()

# @register.filter(name='get_review_photos')
# def get_review_photos(id):
#     photos = ReviewPhotos.objects.filter(ReviewPhotos__review_id=id).photo_path
#     return {'photos': photos}