# File created by F W R Marsh on 04/04/2020
# File is a model description of the database

from django.db import models
from django.contrib.auth.models import User  # import the User table
from django.forms.models import model_to_dict
from PIL import Image

from .uploads import process_uploaded_image, remove_unused_image

# Describes the Hall table


class Hall(models.Model):
    name = models.CharField(max_length=30)
    text = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    campus = models.CharField(max_length=30)
    # below argument ensures only creation date stored
    date_created = models.DateTimeField(auto_now_add=True)
    # below argument ensures last modified date stored
    date_modified = models.DateTimeField(auto_now=True)

    def get_card_data(self):
        hall = model_to_dict(self)
        hall['main_photo'] = self.hallphotos_set.first()
        return hall

    def __str__(self):
        return f'{self.name} - {self.campus}'


# Desribes the HallPhotos table
class HallPhotos(models.Model):
    # TODO: Add thumbnails
    # below will store the path to any photos of halls
    photo_path = models.ImageField(max_length=100, upload_to='uploads/')
    # below will store a brief description of the corresponding photo
    photo_desc = models.TextField()
    # foreign key for the Hall class, on_delete removes record if hall deleted
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super(HallPhotos, self).__init__(*args, **kwargs)
        # Save the initial ImageField to compare when saving
        self._original_photo_path = self.photo_path

    def get_main_photo(hall_id):
        return HallPhotos.filter(hall_id=hall_id)[0]

    def save(self, update_fields=None, **kwargs):
        # TODO: Check for badly-made images (strange aspect ratio etc.)
        super().save(**kwargs)
        # If the photo_path field was updated
        if update_fields is None or 'photo_path' in update_fields:
            # Get the path to the image file
            filename = self.photo_path.path
            # and the ImageField saved on construction
            old_photo = self._original_photo_path
            # Process the image (optimize)
            process_uploaded_image(filename)
            # Check if we had a valid image before that
            if (old_photo is not None and old_photo.name != ''
                    and old_photo.path != filename):
                # And delete it to save space
                remove_unused_image(old_photo.path)


# Describes the RoomType table
class RoomType(models.Model):
    price = models.IntegerField()  # price is stored in pence!
    contract_length = models.IntegerField()
    ensuite = models.BooleanField()
    basin = models.BooleanField()
    bedsize = models.CharField(max_length=30)
    catered = models.BooleanField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    @property
    def formatted_price(self):
        return "%.2f" % (self.price / 100)

    def __str__(self):
        return f'{self.contract_length} weeks @ {int(self.price) / 100} ppw'


# Describes the Review table
class Review(models.Model):
    text = models.TextField()
    # below argument ensures only creation date stored
    date_created = models.DateTimeField(auto_now_add=True)
    # below argument ensures last modified date stored
    date_modified = models.DateTimeField(auto_now=True)
    anonymous = models.BooleanField()
    reported = models.BooleanField(default=False)
    cleanliness = models.IntegerField()
    social_life = models.IntegerField()
    noise = models.IntegerField()
    facilities = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roomtype = models.ForeignKey(RoomType, on_delete=models.CASCADE)

    def __str__(self):
        return f'#{self.id} for {self.roomtype.hall.name} by {self.user.username}'


# Describes the ReviewPhotos table
class ReviewPhotos(models.Model):
    # below will store the path to any photos of halls
    photo_path = models.ImageField(max_length=100, upload_to='review-uploads/')
    # below will store a brief description of the corresponding photo
    photo_desc = models.TextField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)