# File created by F W R Marsh on 04/04/2020
# File is a model description of the database

from django.db import models
from django.contrib.auth.models import User  # import the User table


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

    def __str__(self):
        return f'[{self.id}] {self.name} - {self.campus}'


# Desribes the HallPhotos table
class HallPhotos(models.Model):
    # below will store the path to any photos of halls
    photo_path = models.CharField(max_length=100)
    # below will store a brief description of the corresponding photo
    photo_desc = models.TextField()
    # foreign key for the Hall class, on_delete removes record if hall deleted
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)


# Describes the RoomType table
class RoomType(models.Model):
    price = models.IntegerField()  # price is stored in pence!
    contract_length = models.IntegerField()
    ensuite = models.BooleanField()
    basin = models.BooleanField()
    bedsize = models.CharField(max_length=30)
    catered = models.BooleanField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)


# Describes the Review table
class Review(models.Model):
    text = models.TextField()
    # below argument ensures only creation date stored
    date_created = models.DateTimeField(auto_now_add=True)
    # below argument ensures last modified date stored
    date_modified = models.DateTimeField(auto_now=True)
    anonymous = models.BooleanField()
    reported = models.BooleanField()
    cleanliness = models.IntegerField()
    social_life = models.IntegerField()
    noise = models.IntegerField()
    facilities = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roomtype = models.ForeignKey(RoomType, on_delete=models.CASCADE)


# Describes the ReviewPhotos table
class ReviewPhotos(models.Model):
    # below will store the path to any photos of halls
    photo_path = models.CharField(max_length=100)
    # below will store a brief description of the corresponding photo
    photo_desc = models.TextField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
