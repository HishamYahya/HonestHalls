from django.db import models

from halls.models import RoomType
from users.models import User

from halls.uploads import (
    process_uploaded_image,
    remove_unused_image,
    create_thumbnail,
    get_thumbnail_filename,
)

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
        return f'#{self.id} for {self.roomtype.hall.name} by {self.user.email}'


# Describes the ReviewPhotos table
class ReviewPhotos(models.Model):
    # below will store the path to any photos of halls
    photo_path = models.ImageField(max_length=100, upload_to='review-uploads/')
    # below will store a brief description of the corresponding photo
    photo_desc = models.TextField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def photo_url(self):
        return self.photo_path.url

    @property
    def thumbnail_url(self):
        return get_thumbnail_filename(self.photo_path.url)

    def __init__(self, *args, **kwargs):
        super(ReviewPhotos, self).__init__(*args, **kwargs)
        # Save the initial ImageField to compare when saving
        self._original_photo_path = self.photo_path

    def save(self, update_fields=None, **kwargs):
        """
        Saves the model to the DB. Processes the photo
        if needed and creates a thumbnail file with a specified suffix.
        """
        super().save(**kwargs)
        # If the photo_path field was updated
        if update_fields is None or 'photo_path' in update_fields:
            # Get the path to the image file
            filename = self.photo_path.path
            # and the ImageField saved on construction
            old_photo = self._original_photo_path
            # Process the image (optimize)
            process_uploaded_image(filename)
            # Also create the thumbnail as a file in
            # the same dir with but with a predefined suffix.
            create_thumbnail(filename)
            # Check if we had a valid image before that
            if (old_photo is not None and old_photo.name != ''
                    and old_photo.path != filename):
                # And delete it to save space
                remove_unused_image(old_photo.path)

class ReviewRating(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.BooleanField() # false is a downvote, true is an upvote


class Report(models.Model):
    title = models.CharField(max_length=75)
    explanation = models.CharField(max_length=2500)
    date_reported = models.DateTimeField(auto_now_add=True)

    # 4:27 video 5: Databases
