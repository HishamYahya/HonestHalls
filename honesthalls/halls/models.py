# File created by F W R Marsh on 04/04/2020
# File is a model description of the database

from django.db import models
from django.db.models import Sum, Count
from django.forms.models import model_to_dict

from users.models import User
from .uploads import (
    process_uploaded_image,
    remove_unused_image,
    create_thumbnail,
    get_thumbnail_filename,
)
from .utils import yesno, expiring_lru_cache

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

    @property
    @expiring_lru_cache(expires_in_seconds=300, maxsize=128)
    def average_rating(self):
        """
        Computes the averate rating for the hall.
        This property is cached and by default is renewed
        if the value is older than 5 minutes (300s).
        """
        from reviews.models import Review

        aggregate_kwargs = {
            'count': Count('id'),
        }
        # We want the sum of each individual rating criteria
        for field in Review.RATING_FIELDS:
            aggregate_kwargs[field] = Sum(field)

        # Execute the query agains the DB.
        aggregate_results = (Review.objects
            .filter(roomtype__hall=self)
            .aggregate(**aggregate_kwargs))
            
        # No reviews have been added for this hall yet
        if aggregate_results['count'] == 0:
            return 0

        # Here we compute the sum of all the individual ratings
        # (cleanliness, social_life, etc.)
        rating_sum = 0
        for field in Review.RATING_FIELDS:
            rating_sum += aggregate_results[field]

        # The average is the total / num of fields / num of halls
        average = rating_sum / (aggregate_results['count'] * len(Review.RATING_FIELDS))
        return average

    @property
    def main_photo_url(self):
        main_photo = self.hallphotos_set.first()
        return main_photo and main_photo.photo_url

    @property
    def main_photo_thumbnail(self):
        main_photo = self.hallphotos_set.first()
        return main_photo and main_photo.thumbnail_url


    def get_preview_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'text': self.text,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'campus': self.campus,
            'photo': self.main_photo_url,
            'thumbnail': self.main_photo_thumbnail,
        }


    def get_card_data(self):
        hall = model_to_dict(self)
        hall['main_photo'] = self.hallphotos_set.first()
        hall['average_rating'] = self.average_rating
        return hall

    def __str__(self):
        return f'{self.name} - {self.campus}'


# Desribes the HallPhotos table
class HallPhotos(models.Model):
    # below will store the path to any photos of halls
    photo_path = models.ImageField(max_length=100, upload_to='uploads/')
    # below will store a brief description of the corresponding photo
    photo_desc = models.TextField()
    # foreign key for the Hall class, on_delete removes record if hall deleted
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    @property
    def photo_url(self):
        return self.photo_path.url

    @property
    def thumbnail_url(self):
        return get_thumbnail_filename(self.photo_path.url)

    def __init__(self, *args, **kwargs):
        super(HallPhotos, self).__init__(*args, **kwargs)
        # Save the initial ImageField to compare when saving
        self._original_photo_path = self.photo_path

    def get_main_photo(hall_id):
        try:
            return HallPhotos.objects.get(hall_id=hall_id)[0]
        except:
            pass

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


# Describes the RoomType table
class RoomType(models.Model):
    price = models.IntegerField()  # price is stored in pence!
    contract_length = models.IntegerField()
    ensuite = models.BooleanField()
    basin = models.BooleanField()
    bedsize = models.CharField(max_length=30)
    catered = models.BooleanField()
    accessible = models.BooleanField(default=None, null=True)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    @property
    def formatted_price(self):
        return "%.2f" % (self.price / 100)

    @property
    def formatted_string(self):
        return (
            yesno(self.catered, "Catered", "Non-catered") +
            yesno(self.ensuite, " ensuite", "") +
            " room " +
            yesno(self.basin, "with basin and ", "with ") +
            str(self.bedsize).lower() +
            " bed for " +
            str(self.contract_length) +
            " weeks at £" +
            self.formatted_price +
            "/week. Accessible? " + 
            yesno(self.accessible, "Yes", "No")
        )

    def __str__(self):
        return self.formatted_string
