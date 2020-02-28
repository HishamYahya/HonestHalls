from django import forms

from halls.models import Review, ReviewPhotos


class ReviewEditForm(forms.ModelForm):
    text = forms.CharField(min_length=50, max_length=2500)
    anonymous = forms.BooleanField(required=False)
    cleanliness = forms.IntegerField(initial=5, min_value=1, max_value=5)
    social_life = forms.IntegerField(initial=5, min_value=1, max_value=5)
    noise = forms.IntegerField(initial=5, min_value=1, max_value=5)
    facilities = forms.IntegerField(initial=5, min_value=1, max_value=5)
    roomtype = forms.IntegerField(min_value=1)

    class Meta:
        model = Review
        fields = ['text', 'anonymous', 'cleanliness',
                  'social_life', 'noise', 'facilities']


class ReviewPhotosEditForm(forms.ModelForm):
    class Meta:
        model = ReviewPhotos
        fields = ['photo_path', 'photo_desc']